#!/usr/bin/env bash

set -uo pipefail

readonly ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DEFAULT_SAMPLE_ROOT="$ROOT_DIR/jaws_bench_dataset/single_file"
readonly DEFAULT_WORKSPACE_ROOT="$ROOT_DIR/workspace_codex/single"
readonly DEFAULT_RUNNER="$ROOT_DIR/run_codex_prompt.sh"
readonly DEFAULT_SANDBOX="workspace-write"
readonly DEFAULT_MODEL="gpt-5.4"
readonly DEFAULT_APPROVAL_MODE="never"
readonly DEFAULT_PROMPT="The workspace contains a file with some incomplete code. Complete the code at the line marked <FILL_HERE>."

usage() {
  cat <<'EOF'
Usage:
  run_codex_single.sh [--sample-root DIR] [--workspace-root DIR] [--sandbox MODE] [--model NAME] [--approval MODE] [--json]

Description:
  Iterate over the single-file benchmark samples, copy each sample directory
  into a fresh workspace at workspace_codex/single/<pid>, and run Codex once with a
  fixed completion prompt against that copied workspace.

Options:
  --sample-root DIR   Root directory containing per-pid sample directories.
                      Default: ./jaws_bench_dataset/single_file
  --workspace-root DIR
                      Root directory for per-pid workspaces.
                      Default: ./workspace_codex/single
  --sandbox MODE      Sandbox mode forwarded to run_codex_prompt.sh.
                      Default: workspace-write
  --model NAME        Codex model override.
                      Default: gpt-5.4
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

validate_dir() {
  local path="$1"
  [[ -d "$path" ]] || fail "Required directory not found: $path"
}

emit_sample_dirs() {
  local sample_root="$1"
  find "$sample_root" -mindepth 1 -maxdepth 1 -type d | sort
}

prepare_workspace_from_sample() {
  local sample_dir="$1"
  local workspace_dir="$2"

  rm -rf -- "$workspace_dir"
  mkdir -p "$workspace_dir"
  cp -R "$sample_dir"/. "$workspace_dir"/
}

run_sample() {
  local runner="$1"
  local sample_dir="$2"
  local workspace_root="$3"
  local sandbox="$4"
  local model="$5"
  local approval_mode="$6"
  local json_enabled="$7"

  local pid
  pid="$(basename "$sample_dir")"

  local workspace_dir="$workspace_root/$pid"
  local -a cmd=(
    "$runner"
    --workspace "$workspace_dir"
    --sandbox "$sandbox"
    --model "$model"
    --approval "$approval_mode"
    --ephemeral
    --prompt "$DEFAULT_PROMPT"
  )

  if [[ "$json_enabled" == "1" ]]; then
    cmd+=(--json)
  fi

  prepare_workspace_from_sample "$sample_dir" "$workspace_dir"
  printf 'Running pid=%s in workspace=%s\n' "$pid" "$workspace_dir" >&2
  "${cmd[@]}" </dev/null
}

process_samples() {
  local sample_root="$1"
  local runner="$2"
  local workspace_root="$3"
  local sandbox="$4"
  local model="$5"
  local approval_mode="$6"
  local json_enabled="$7"
  local failures_ref="$8"

  local sample_dir=""
  local total_runs=0
  local failed_runs=0
  local pid=""

  while IFS= read -r sample_dir; do
    [[ -n "$sample_dir" ]] || continue
    total_runs=$((total_runs + 1))
    pid="$(basename "$sample_dir")"

    if ! run_sample "$runner" "$sample_dir" "$workspace_root" "$sandbox" "$model" "$approval_mode" "$json_enabled"; then
      printf 'pid=%s failed\n' "$pid" >&2
      failed_runs=$((failed_runs + 1))
      printf -v "$failures_ref" '%s %s' "${!failures_ref}" "$pid"
    fi
  done < <(emit_sample_dirs "$sample_root")

  printf 'Finished %s: total=%d failed=%d succeeded=%d\n' \
    "$sample_root" \
    "$total_runs" \
    "$failed_runs" \
    "$((total_runs - failed_runs))" >&2
}

main() {
  local sample_root="$DEFAULT_SAMPLE_ROOT"
  local workspace_root="$DEFAULT_WORKSPACE_ROOT"
  local runner="$DEFAULT_RUNNER"
  local sandbox="$DEFAULT_SANDBOX"
  local model="$DEFAULT_MODEL"
  local approval_mode="$DEFAULT_APPROVAL_MODE"
  local json_enabled="0"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --sample-root)
        [[ $# -ge 2 ]] || fail "--sample-root requires a value"
        sample_root="$2"
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
  require_command cp
  require_command find
  require_command sort
  validate_dir "$sample_root"
  validate_dir "$(dirname "$runner")"
  [[ -f "$runner" ]] || fail "Required runner not found: $runner"
  mkdir -p "$workspace_root"

  local failures=""
  printf 'Processing %s\n' "$sample_root" >&2
  process_samples "$sample_root" "$runner" "$workspace_root" "$sandbox" "$model" "$approval_mode" "$json_enabled" failures

  if [[ -n "${failures// }" ]]; then
    printf 'Completed with failures for pid(s):%s\n' "$failures" >&2
    exit 1
  fi
}

main "$@"
