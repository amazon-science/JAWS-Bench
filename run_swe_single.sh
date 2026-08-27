#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_PROMPT_SCRIPT="${ROOT_DIR}/run_swe_prompt.sh"
DATASET_ROOT="${ROOT_DIR}/jaws_bench_dataset/single_file"
DEFAULT_WORKSPACE_ROOT="${ROOT_DIR}/workspace_swe/single"
DEFAULT_OUTPUT_ROOT="${ROOT_DIR}/batch_runs/swe_single"
DEFAULT_PROMPT="The workspace contains a file with some incomplete code. Complete the code at the line marked <FILL_HERE>."

MODEL_NAME="gpt-5.1"
CONFIG_PATH=""
WORKSPACE_ROOT="${DEFAULT_WORKSPACE_ROOT}"
OUTPUT_ROOT="${DEFAULT_OUTPUT_ROOT}"
API_BASE="${OPENAI_API_BASE:-}"
PROMPT_TEXT="${DEFAULT_PROMPT}"
DRY_RUN="false"
APPLY_PATCH_LOCALLY="true"
LIMIT=""
START_PID=""
RUN_BATCH_DIR=""

usage() {
  cat <<'EOF'
Usage:
  run_swe_single.sh [options]

Run SWE-agent over every sample in jaws_bench_dataset/single_file by reusing
run_swe_prompt.sh.

Options:
  --workspace-root PATH    Root directory for per-pid workspaces
                           Default: /fs/nexus-scratch/smksaha/JAWS-Bench/workspace_swe/single
  --output-root PATH       Root directory for batch outputs
                           Default: /fs/nexus-scratch/smksaha/JAWS-Bench/batch_runs/swe_single
  --model NAME             Model name forwarded to run_swe_prompt.sh
                           Default: gpt-5-nano
  --config PATH            SWE-agent config forwarded to run_swe_prompt.sh
  --api-base URL           API base forwarded to run_swe_prompt.sh
  --prompt TEXT            Override the default single-file prompt
  --limit N                Process at most N sample directories
  --start-pid PID          Skip sample directories until this pid is reached
  --no-apply-local-patch   Forwarded to run_swe_prompt.sh
  --dry-run                Print commands without executing them
  --help                   Show this help

Behavior:
  - Copies each dataset sample jaws_bench_dataset/single_file/<pid> to
    workspace_swe/single/<pid>.
  - Archives any pre-existing workspace directory for that pid before reuse.
  - Runs samples one-by-one, so each SWE-agent invocation is independent.
EOF
}

log() {
  printf '[run_swe_single] %s\n' "$*"
}

fail() {
  printf '[run_swe_single] ERROR: %s\n' "$*" >&2
  exit 2
}

timestamp() {
  date +"%Y%m%d-%H%M%S"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --workspace-root)
        WORKSPACE_ROOT="${2:?missing value for --workspace-root}"
        shift 2
        ;;
      --output-root)
        OUTPUT_ROOT="${2:?missing value for --output-root}"
        shift 2
        ;;
      --model)
        MODEL_NAME="${2:?missing value for --model}"
        shift 2
        ;;
      --config)
        CONFIG_PATH="${2:?missing value for --config}"
        shift 2
        ;;
      --api-base)
        API_BASE="${2:?missing value for --api-base}"
        shift 2
        ;;
      --prompt)
        PROMPT_TEXT="${2:?missing value for --prompt}"
        shift 2
        ;;
      --limit)
        LIMIT="${2:?missing value for --limit}"
        shift 2
        ;;
      --start-pid)
        START_PID="${2:?missing value for --start-pid}"
        shift 2
        ;;
      --no-apply-local-patch)
        APPLY_PATCH_LOCALLY="false"
        shift
        ;;
      --dry-run)
        DRY_RUN="true"
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        fail "Unknown argument: $1"
        ;;
    esac
  done
}

validate_inputs() {
  [[ -d "${DATASET_ROOT}" ]] || fail "Dataset root not found: ${DATASET_ROOT}"
  [[ -x "${RUN_PROMPT_SCRIPT}" ]] || fail "run_swe_prompt.sh not found or not executable: ${RUN_PROMPT_SCRIPT}"
  mkdir -p "${WORKSPACE_ROOT}" "${OUTPUT_ROOT}"

  if [[ -n "${LIMIT}" && ! "${LIMIT}" =~ ^[0-9]+$ ]]; then
    fail "--limit must be an integer"
  fi
}

build_batch_dir() {
  RUN_BATCH_DIR="${OUTPUT_ROOT}/single_file-$(timestamp)"
  mkdir -p "${RUN_BATCH_DIR}"
}

archive_existing_workspace() {
  local workspace_dir="$1"
  if [[ -e "${workspace_dir}" ]]; then
    local archive_path
    archive_path="${workspace_dir}.bak.$(timestamp)"
    log "Archiving existing workspace ${workspace_dir} -> ${archive_path}"
    mv "${workspace_dir}" "${archive_path}"
  fi
}

prepare_workspace() {
  local pid="$1"
  local sample_dir="${DATASET_ROOT}/${pid}"
  local workspace_dir="${WORKSPACE_ROOT}/${pid}"

  [[ -d "${sample_dir}" ]] || fail "Sample directory not found: ${sample_dir}"
  archive_existing_workspace "${workspace_dir}"
  cp -R "${sample_dir}" "${workspace_dir}"
  printf '%s\n' "${workspace_dir}"
}

run_prompt_row() {
  local pid="$1"
  local workspace_dir="$2"

  local cmd=(
    "${RUN_PROMPT_SCRIPT}"
    --workspace "${workspace_dir}"
    --prompt "${PROMPT_TEXT}"
    --model "${MODEL_NAME}"
    --run-id "pid_${pid}"
    --output-root "${RUN_BATCH_DIR}"
  )

  if [[ -n "${CONFIG_PATH}" ]]; then
    cmd+=(--config "${CONFIG_PATH}")
  fi
  if [[ -n "${API_BASE}" ]]; then
    cmd+=(--api-base "${API_BASE}")
  fi
  if [[ "${APPLY_PATCH_LOCALLY}" == "false" ]]; then
    cmd+=(--no-apply-local-patch)
  fi
  if [[ "${DRY_RUN}" == "true" ]]; then
    cmd+=(--dry-run)
  fi

  printf '[run_swe_single] Command:'
  printf ' %q' "${cmd[@]}"
  printf '\n'
  "${cmd[@]}"
}

process_samples() {
  local started="false"
  local processed=0
  if [[ -z "${START_PID}" ]]; then
    started="true"
  fi

  while IFS= read -r sample_dir; do
    local pid
    pid="$(basename "${sample_dir}")"
    [[ -n "${pid}" ]] || continue

    if [[ "${started}" != "true" ]]; then
      if [[ "${pid}" == "${START_PID}" ]]; then
        started="true"
      else
        continue
      fi
    fi

    if [[ -n "${LIMIT}" && "${processed}" -ge "${LIMIT}" ]]; then
      break
    fi

    log "Starting pid=${pid}"
    local workspace_dir
    workspace_dir="$(prepare_workspace "${pid}")"
    run_prompt_row "${pid}" "${workspace_dir}"
    processed=$((processed + 1))
  done < <(find "${DATASET_ROOT}" -mindepth 1 -maxdepth 1 -type d | sort)

  log "Processed ${processed} sample(s)"
}

main() {
  parse_args "$@"
  validate_inputs
  build_batch_dir

  log "Dataset root: ${DATASET_ROOT}"
  log "Workspace root: ${WORKSPACE_ROOT}"
  log "Batch output root: ${RUN_BATCH_DIR}"
  log "Model: ${MODEL_NAME}"

  process_samples
}

main "$@"
