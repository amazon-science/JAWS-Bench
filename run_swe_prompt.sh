#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWE_AGENT_DIR="${ROOT_DIR}/SWE-agent"
DEFAULT_CONFIG="${SWE_AGENT_DIR}/config/default.yaml"
DEFAULT_OUTPUT_ROOT="${ROOT_DIR}/batch_runs/swe_prompt"

WORKSPACE_PATH="${ROOT_DIR}/workspace_swe/"
PROMPT_TEXT="Implement a python program that takes a list of integers and returns the max of all numbers in the list."
MODEL_NAME="gpt-5.1"
CONFIG_PATH="${DEFAULT_CONFIG}"
OUTPUT_ROOT="${DEFAULT_OUTPUT_ROOT}"
RUN_ID=""
DRY_RUN="false"
EXTRA_CONFIG_PATH=""
API_BASE="${OPENAI_API_BASE:-}"
APPLY_PATCH_LOCALLY="true"

usage() {
  cat <<'EOF'
Usage:
  run_swe_prompt.sh [options]

Run SWE-agent on a single plain-text prompt for one workspace.

Options:
  --workspace PATH       Workspace directory to use for this run
                         Default placeholder: /abs/path/to/workspace
  --prompt TEXT          Plain-text prompt for SWE-agent
                         Default placeholder: replace this with your prompt
  --model NAME           Model name to pass to SWE-agent
                         Default: gpt-4o
  --config PATH          SWE-agent config file
                         Default: /fs/nexus-scratch/smksaha/JAWS-Bench/SWE-agent/config/default.yaml
  --output-root PATH     Root directory for run outputs
                         Default: /fs/nexus-scratch/smksaha/JAWS-Bench/batch_runs/swe_prompt
  --run-id ID            Optional run identifier
  --api-base URL         Override the model API base URL
                         Default: \$OPENAI_API_BASE or auto-selected for GPT-5
  --no-apply-local-patch Do not apply the resulting patch back to the workspace
  --dry-run              Print the command without executing it
  --help                 Show this help

Notes:
  - SWE-agent expects --env.repo.path to point to a git repository.
  - This script will automatically initialize a git repo for the workspace
    if one does not exist yet.
  - Existing git repos should be clean before running, or SWE-agent may refuse
    to copy them.
EOF
}

log() {
  printf '[run_swe_prompt] %s\n' "$*"
}

fail() {
  printf '[run_swe_prompt] ERROR: %s\n' "$*" >&2
  exit 2
}

timestamp() {
  date +"%Y%m%d-%H%M%S"
}

cleanup() {
  if [[ -n "${EXTRA_CONFIG_PATH}" && -f "${EXTRA_CONFIG_PATH}" ]]; then
    rm -f "${EXTRA_CONFIG_PATH}"
  fi
}

trap cleanup EXIT

is_git_repo() {
  git -C "${WORKSPACE_PATH}" rev-parse --show-toplevel >/dev/null 2>&1
}

repo_has_commits() {
  git -C "${WORKSPACE_PATH}" rev-parse --verify HEAD >/dev/null 2>&1
}

repo_has_tracked_files() {
  [[ -n "$(git -C "${WORKSPACE_PATH}" ls-files)" ]]
}

bootstrap_placeholder_file() {
  local placeholder_path
  placeholder_path="${WORKSPACE_PATH}/.swe-agent-bootstrap"
  if [[ ! -e "${placeholder_path}" ]]; then
    printf 'Workspace bootstrap file for SWE-agent.\n' > "${placeholder_path}"
  fi
}

ensure_bootstrap_gitignore() {
  local gitignore_path
  gitignore_path="${WORKSPACE_PATH}/.gitignore"

  if [[ ! -e "${gitignore_path}" ]]; then
    cat > "${gitignore_path}" <<'EOF'
__pycache__/
*.pyc
EOF
    return
  fi

  if ! grep -qxF "__pycache__/" "${gitignore_path}"; then
    printf '\n__pycache__/\n' >> "${gitignore_path}"
  fi
  if ! grep -qxF "*.pyc" "${gitignore_path}"; then
    printf '*.pyc\n' >> "${gitignore_path}"
  fi
}

cleanup_python_cache_files() {
  find "${WORKSPACE_PATH}" -type d -name "__pycache__" -prune -exec rm -rf {} +
  find "${WORKSPACE_PATH}" -type f -name "*.pyc" -delete
}

ensure_repo_has_initial_commit() {
  ensure_bootstrap_gitignore
  cleanup_python_cache_files
  git -C "${WORKSPACE_PATH}" add .gitignore

  if ! repo_has_tracked_files; then
    bootstrap_placeholder_file
    git -C "${WORKSPACE_PATH}" add .swe-agent-bootstrap
  fi

  if ! repo_has_commits || [[ -n "$(git -C "${WORKSPACE_PATH}" status --porcelain)" ]]; then
    git -C "${WORKSPACE_PATH}" commit -m "Initialize workspace for SWE-agent" >/dev/null
  fi
}

ensure_git_repo() {
  if ! is_git_repo; then
    log "Workspace is not a git repo. Initializing one at ${WORKSPACE_PATH}"
    git -C "${WORKSPACE_PATH}" init >/dev/null
  fi

  git -C "${WORKSPACE_PATH}" add -A
  ensure_repo_has_initial_commit
}

ensure_clean_repo() {
  if [[ -n "$(git -C "${WORKSPACE_PATH}" status --porcelain)" ]]; then
    fail "Workspace git repo is not clean: ${WORKSPACE_PATH}. Commit or stash changes before running SWE-agent."
  fi
}

model_needs_top_p_disabled() {
  [[ "${MODEL_NAME}" == gpt-5* ]]
}

resolve_api_base() {
  if [[ -n "${API_BASE}" ]]; then
    printf '%s\n' "${API_BASE}"
    return
  fi

  if [[ "${MODEL_NAME}" == gpt-5* ]]; then
    printf '%s\n' "https://us.api.openai.com/v1"
    return
  fi

  printf '\n'
}

prepare_runtime_config() {
  CONFIG_ARGS=(--config "${CONFIG_PATH}")
  local resolved_api_base
  resolved_api_base="$(resolve_api_base)"

  if model_needs_top_p_disabled; then
    EXTRA_CONFIG_PATH="$(mktemp /tmp/run_swe_prompt.XXXXXX.yaml)"
    cat > "${EXTRA_CONFIG_PATH}" <<EOF
agent:
  model:
    top_p: null
    temperature: 1.0
EOF
    if [[ -n "${resolved_api_base}" ]]; then
      cat >> "${EXTRA_CONFIG_PATH}" <<EOF
    api_base: ${resolved_api_base}
EOF
    fi
    CONFIG_ARGS+=(--config "${EXTRA_CONFIG_PATH}")
    log "Created runtime config override for ${MODEL_NAME} at ${EXTRA_CONFIG_PATH}"
  elif [[ -n "${resolved_api_base}" ]]; then
    EXTRA_CONFIG_PATH="$(mktemp /tmp/run_swe_prompt.XXXXXX.yaml)"
    cat > "${EXTRA_CONFIG_PATH}" <<EOF
agent:
  model:
    api_base: ${resolved_api_base}
EOF
    CONFIG_ARGS+=(--config "${EXTRA_CONFIG_PATH}")
    log "Created runtime config override for api_base at ${EXTRA_CONFIG_PATH}"
  fi
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --workspace)
        WORKSPACE_PATH="${2:?missing value for --workspace}"
        shift 2
        ;;
      --prompt)
        PROMPT_TEXT="${2:?missing value for --prompt}"
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
      --output-root)
        OUTPUT_ROOT="${2:?missing value for --output-root}"
        shift 2
        ;;
      --run-id)
        RUN_ID="${2:?missing value for --run-id}"
        shift 2
        ;;
      --api-base)
        API_BASE="${2:?missing value for --api-base}"
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
  [[ -d "${SWE_AGENT_DIR}" ]] || fail "SWE-agent directory not found: ${SWE_AGENT_DIR}"
  [[ -f "${CONFIG_PATH}" ]] || fail "Config file not found: ${CONFIG_PATH}"

  if [[ "${WORKSPACE_PATH}" == "/abs/path/to/workspace" ]]; then
    fail "Replace the placeholder workspace path before running."
  fi
  if [[ "${PROMPT_TEXT}" == "replace this with your prompt" ]]; then
    fail "Replace the placeholder prompt before running."
  fi

  [[ -d "${WORKSPACE_PATH}" ]] || fail "Workspace directory not found: ${WORKSPACE_PATH}"
  ensure_git_repo
  ensure_clean_repo
}

build_run_context() {
  local effective_run_id
  effective_run_id="${RUN_ID:-run-$(timestamp)}"
  RUN_OUTPUT_DIR="${OUTPUT_ROOT}/${effective_run_id}"
}

build_command() {
  SWE_CMD=(
    sweagent
    run
    "${CONFIG_ARGS[@]}"
    --agent.model.name "${MODEL_NAME}"
    --env.repo.path "${WORKSPACE_PATH}"
    --problem_statement.text "${PROMPT_TEXT}"
    --output_dir "${RUN_OUTPUT_DIR}"
  )

  if [[ "${APPLY_PATCH_LOCALLY}" == "true" ]]; then
    SWE_CMD+=(--actions.apply_patch_locally true)
  fi
}

print_command() {
  printf 'Command:'
  printf ' %q' "${SWE_CMD[@]}"
  printf '\n'
}

execute_run() {
  mkdir -p "${RUN_OUTPUT_DIR}"
  (
    cd "${SWE_AGENT_DIR}"
    "${SWE_CMD[@]}"
  )
}

sanitize_patch_file() {
  local source_patch="$1"
  local sanitized_patch="$2"

  awk '
    /^diff --git / {
      if ($0 ~ /(^| )a\/__pycache__\// || $0 ~ /(^| )b\/__pycache__\// || $0 ~ /\.pyc( |$)/) {
        skip = 1
      } else {
        skip = 0
      }
    }
    !skip { print }
  ' "${source_patch}" > "${sanitized_patch}"
}

apply_saved_patch_fallback() {
  if [[ "${APPLY_PATCH_LOCALLY}" != "true" ]]; then
    return
  fi

  local patch_file
  patch_file="$(find "${RUN_OUTPUT_DIR}" -type f -name '*.patch' | head -n 1 || true)"
  if [[ -z "${patch_file}" ]]; then
    return
  fi

  local sanitized_patch
  sanitized_patch="$(mktemp /tmp/run_swe_prompt_patch.XXXXXX.patch)"
  sanitize_patch_file "${patch_file}" "${sanitized_patch}"

  if git -C "${WORKSPACE_PATH}" apply --check "${sanitized_patch}" >/dev/null 2>&1; then
    log "Applying sanitized patch fallback to workspace"
    git -C "${WORKSPACE_PATH}" apply "${sanitized_patch}"
  fi

  rm -f "${sanitized_patch}"
}

main() {
  parse_args "$@"
  validate_inputs
  build_run_context
  prepare_runtime_config
  build_command

  log "Workspace: ${WORKSPACE_PATH}"
  log "Output dir: ${RUN_OUTPUT_DIR}"
  log "Model: ${MODEL_NAME}"
  log "Apply patch locally: ${APPLY_PATCH_LOCALLY}"

  if [[ "${DRY_RUN}" == "true" ]]; then
    print_command
    exit 0
  fi

  print_command
  execute_run
  apply_saved_patch_fallback
}

main "$@"
