#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_PROMPT_SCRIPT="${ROOT_DIR}/run_swe_prompt.sh"
DEFAULT_WORKSPACE_ROOT="${ROOT_DIR}/workspace_swe/empty"
DEFAULT_OUTPUT_ROOT="${ROOT_DIR}/batch_runs/swe_empty"

CSV_PATH="${ROOT_DIR}/jaws_bench_dataset/empty/t2c_l1.csv"
MODEL_NAME="gpt-5.1"
CONFIG_PATH=""
WORKSPACE_ROOT="${DEFAULT_WORKSPACE_ROOT}"
OUTPUT_ROOT="${DEFAULT_OUTPUT_ROOT}"
API_BASE="${OPENAI_API_BASE:-}"
DRY_RUN="false"
APPLY_PATCH_LOCALLY="true"
LIMIT=""
START_PID=""
MANIFEST_PATH=""
RUN_BATCH_DIR=""

usage() {
  cat <<'EOF'
Usage:
  run_swe_empty.sh --csv PATH [options]

Run SWE-agent over every row in a JAWS-Bench empty-subset CSV by reusing
run_swe_prompt.sh.

Options:
  --csv PATH               Path to an empty-subset CSV file
  --workspace-root PATH    Root directory for per-pid workspaces
                           Default: /fs/nexus-scratch/smksaha/JAWS-Bench/workspace_swe/empty
  --output-root PATH       Root directory for batch outputs
                           Default: /fs/nexus-scratch/smksaha/JAWS-Bench/batch_runs/swe_empty
  --model NAME             Model name forwarded to run_swe_prompt.sh
                           Default: gpt-5-nano
  --config PATH            SWE-agent config forwarded to run_swe_prompt.sh
  --api-base URL           API base forwarded to run_swe_prompt.sh
  --limit N                Process at most N rows
  --start-pid PID          Skip rows until this pid is reached
  --no-apply-local-patch   Forwarded to run_swe_prompt.sh
  --dry-run                Print commands without executing them
  --help                   Show this help

Behavior:
  - Reads only the `pid` and `prompt` columns from the CSV.
  - Creates a fresh workspace at workspace_swe/empty/<pid> for each row.
  - Archives any pre-existing workspace directory for that pid before reuse.
  - Runs rows one-by-one, so each SWE-agent invocation is independent.
EOF
}

log() {
  printf '[run_swe_empty] %s\n' "$*"
}

fail() {
  printf '[run_swe_empty] ERROR: %s\n' "$*" >&2
  exit 2
}

timestamp() {
  date +"%Y%m%d-%H%M%S"
}

cleanup() {
  if [[ -n "${MANIFEST_PATH}" && -f "${MANIFEST_PATH}" ]]; then
    rm -f "${MANIFEST_PATH}"
  fi
}

trap cleanup EXIT

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --csv)
        CSV_PATH="${2:?missing value for --csv}"
        shift 2
        ;;
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
  [[ -n "${CSV_PATH}" ]] || fail "--csv is required"
  [[ -f "${CSV_PATH}" ]] || fail "CSV file not found: ${CSV_PATH}"
  [[ -x "${RUN_PROMPT_SCRIPT}" ]] || fail "run_swe_prompt.sh not found or not executable: ${RUN_PROMPT_SCRIPT}"
  mkdir -p "${WORKSPACE_ROOT}" "${OUTPUT_ROOT}"

  if [[ -n "${LIMIT}" && ! "${LIMIT}" =~ ^[0-9]+$ ]]; then
    fail "--limit must be an integer"
  fi
}

build_batch_dir() {
  local csv_stem
  csv_stem="$(basename "${CSV_PATH}")"
  csv_stem="${csv_stem%.csv}"
  RUN_BATCH_DIR="${OUTPUT_ROOT}/${csv_stem}-$(timestamp)"
  mkdir -p "${RUN_BATCH_DIR}"
}

export_manifest() {
  MANIFEST_PATH="$(mktemp /tmp/run_swe_empty.XXXXXX.tsv)"
  python3 - "${CSV_PATH}" "${MANIFEST_PATH}" <<'PY'
import csv
import sys
from pathlib import Path

csv_path = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])

with csv_path.open(newline="", encoding="utf-8") as infile, manifest_path.open("w", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    if "pid" not in reader.fieldnames or "prompt" not in reader.fieldnames:
        raise SystemExit("CSV must contain `pid` and `prompt` columns")
    for row in reader:
        pid = (row.get("pid") or "").strip()
        prompt = (row.get("prompt") or "").replace("\r", " ").replace("\n", " ").strip()
        if not pid or not prompt:
            continue
        outfile.write(f"{pid}\t{prompt}\n")
PY
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
  local workspace_dir="${WORKSPACE_ROOT}/${pid}"
  archive_existing_workspace "${workspace_dir}"
  mkdir -p "${workspace_dir}"
  printf '%s\n' "${workspace_dir}"
}

run_prompt_row() {
  local pid="$1"
  local prompt="$2"
  local workspace_dir="$3"
  local row_output_root="${RUN_BATCH_DIR}"

  local cmd=(
    "${RUN_PROMPT_SCRIPT}"
    --workspace "${workspace_dir}"
    --prompt "${prompt}"
    --model "${MODEL_NAME}"
    --run-id "pid_${pid}"
    --output-root "${row_output_root}"
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

  printf '[run_swe_empty] Command:'
  printf ' %q' "${cmd[@]}"
  printf '\n'
  "${cmd[@]}"
}

process_rows() {
  local started="false"
  local processed=0
  if [[ -z "${START_PID}" ]]; then
    started="true"
  fi

  while IFS=$'\t' read -r pid prompt; do
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
    run_prompt_row "${pid}" "${prompt}" "${workspace_dir}"
    processed=$((processed + 1))
  done < "${MANIFEST_PATH}"

  log "Processed ${processed} row(s)"
}

main() {
  parse_args "$@"
  validate_inputs
  build_batch_dir
  export_manifest

  log "CSV: ${CSV_PATH}"
  log "Workspace root: ${WORKSPACE_ROOT}"
  log "Batch output root: ${RUN_BATCH_DIR}"
  log "Model: ${MODEL_NAME}"

  process_rows
}

main "$@"