#!/usr/bin/env bash

set -uo pipefail

readonly ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DEFAULT_CSV_FILE="$ROOT_DIR/jaws_bench_dataset/empty/t2c_l2.csv"
readonly DEFAULT_WORKSPACE_ROOT="$ROOT_DIR/workspace_codex/empty"
readonly DEFAULT_RUNNER="$ROOT_DIR/run_codex_prompt.sh"
readonly DEFAULT_SANDBOX="workspace-write"
readonly DEFAULT_MODEL="gpt-5.4"
readonly DEFAULT_APPROVAL_MODE="never"

usage() {
  cat <<'EOF'
Usage:
  run_codex_empty.sh [--csv-file PATH] [--workspace-root DIR] [--sandbox MODE] [--json]

Description:
  Read an empty-subset CSV file, extract each row's pid and prompt, create a
  fresh empty workspace at workspace_codex/empty/<pid>, and run Codex once for
  that prompt in that workspace.

Options:
  --csv-file PATH     CSV file to process.
                      Default: ./jaws_bench_dataset/empty/t2c_l2.csv
  --workspace-root DIR
                      Root directory for per-pid workspaces.
                      Default: ./workspace_codex/empty
  --sandbox MODE      Sandbox mode forwarded to run_codex_prompt.sh.
                      Default: workspace-write
  --model NAME        Codex model override.
                      Default: gpt-5-mini
  --approval MODE     Approval mode forwarded to run_codex_prompt.sh.
                      Default: never
  --json              Forward --json to run_codex_prompt.sh.
  --help, -h          Show this help message.
EOF
}

fail() {
  printf 'Error: %s\n' "$1" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

validate_file() {
  local path="$1"
  [[ -f "$path" ]] || fail "Required file not found: $path"
}

emit_pid_prompt_pairs() {
  local csv_path="$1"

  python3 - "$csv_path" <<'PY'
import csv
import sys

csv_path = sys.argv[1]

with open(csv_path, newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    for row in reader:
        pid = (row.get("pid") or "").strip()
        prompt = (row.get("prompt") or "").strip()
        if not pid or not prompt:
            continue
        sys.stdout.write(pid)
        sys.stdout.write("\0")
        sys.stdout.write(prompt)
        sys.stdout.write("\0")
PY
}

prepare_workspace() {
  local workspace_dir="$1"
  rm -rf -- "$workspace_dir"
  mkdir -p "$workspace_dir"
}

run_sample() {
  local runner="$1"
  local workspace_root="$2"
  local sandbox="$3"
  local model="$4"
  local approval_mode="$5"
  local json_enabled="$6"
  local pid="$7"
  local prompt="$8"

  local workspace_dir="$workspace_root/$pid"
  local -a cmd=(
    "$runner"
    --workspace "$workspace_dir"
    --sandbox "$sandbox"
    --model "$model"
    --approval "$approval_mode"
    --ephemeral
    --prompt "$prompt"
  )

  if [[ "$json_enabled" == "1" ]]; then
    cmd+=(--json)
  fi

  prepare_workspace "$workspace_dir"
  printf 'Running pid=%s in workspace=%s\n' "$pid" "$workspace_dir" >&2
  "${cmd[@]}" </dev/null
}

process_csv() {
  local csv_path="$1"
  local runner="$2"
  local workspace_root="$3"
  local sandbox="$4"
  local model="$5"
  local approval_mode="$6"
  local json_enabled="$7"
  local failures_ref="$8"

  local pid=""
  local prompt=""
  local total_runs=0
  local failed_runs=0

  while IFS= read -r -d '' pid && IFS= read -r -d '' prompt; do
    total_runs=$((total_runs + 1))
    if ! run_sample "$runner" "$workspace_root" "$sandbox" "$model" "$approval_mode" "$json_enabled" "$pid" "$prompt"; then
      printf 'pid=%s failed\n' "$pid" >&2
      failed_runs=$((failed_runs + 1))
      printf -v "$failures_ref" '%s %s' "${!failures_ref}" "$pid"
    fi
  done < <(emit_pid_prompt_pairs "$csv_path")

  printf 'Finished %s: total=%d failed=%d succeeded=%d\n' \
    "$csv_path" \
    "$total_runs" \
    "$failed_runs" \
    "$((total_runs - failed_runs))" >&2
}

main() {
  local csv_file="$DEFAULT_CSV_FILE"
  local workspace_root="$DEFAULT_WORKSPACE_ROOT"
  local runner="$DEFAULT_RUNNER"
  local sandbox="$DEFAULT_SANDBOX"
  local model="$DEFAULT_MODEL"
  local approval_mode="$DEFAULT_APPROVAL_MODE"
  local json_enabled="0"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --csv-file)
        [[ $# -ge 2 ]] || fail "--csv-file requires a value"
        csv_file="$2"
        shift 2
        ;;
      --workspace-root)
        [[ $# -ge 2 ]] || fail "--workspace-root requires a value"
        workspace_root="$2"
        shift 2
        ;;
      --runner)
        [[ $# -ge 2 ]] || fail "--runner requires a value"
        runner="$2"
        shift 2
        ;;
      --sandbox)
        [[ $# -ge 2 ]] || fail "--sandbox requires a value"
        sandbox="$2"
        shift 2
        ;;
      --model)
        [[ $# -ge 2 ]] || fail "--model requires a value"
        model="$2"
        shift 2
        ;;
      --approval)
        [[ $# -ge 2 ]] || fail "--approval requires a value"
        approval_mode="$2"
        shift 2
        ;;
      --json)
        json_enabled="1"
        shift
        ;;
      --help|-h)
        usage
        exit 0
        ;;
      --*)
        fail "Unknown option: $1"
        ;;
      *)
        fail "Unexpected argument: $1"
        ;;
    esac
  done

  require_command bash
  require_command python3
  validate_file "$runner"
  validate_file "$csv_file"
  mkdir -p "$workspace_root"

  local failures=""
  printf 'Processing %s\n' "$csv_file" >&2
  process_csv "$csv_file" "$runner" "$workspace_root" "$sandbox" "$model" "$approval_mode" "$json_enabled" failures

  if [[ -n "${failures// }" ]]; then
    printf 'Completed with failures for pid(s):%s\n' "$failures" >&2
    exit 1
  fi
}

main "$@"
