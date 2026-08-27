#!/usr/bin/env bash

set -euo pipefail

readonly DEFAULT_WORKSPACE=""
readonly DEFAULT_SANDBOX="workspace-write"
readonly DEFAULT_MODEL=""
readonly DEFAULT_APPROVAL_MODE=""
readonly DEFAULT_EPHEMERAL="0"

usage() {
  cat <<'EOF'
Usage:
  run_codex_prompt.sh --prompt "your prompt here" [--workspace DIR] [--sandbox MODE] [--model NAME] [--approval MODE] [--ephemeral] [--json]
  run_codex_prompt.sh "your prompt here" [--workspace DIR] [--sandbox MODE] [--model NAME] [--approval MODE] [--ephemeral] [--json]

Description:
  Run Codex on a single prompt against a specific workspace directory.

Options:
  --prompt TEXT       Prompt to send to Codex.
  --workspace DIR     Workspace for the Codex run.
                      Required unless a default workspace is configured.
  --sandbox MODE      Codex sandbox mode. Default: workspace-write
  --model NAME        Codex model override.
  --approval MODE     Approval mode passed as --ask-for-approval.
  --ephemeral         Run Codex in ephemeral mode.
  --json              Emit Codex JSONL output.
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

validate_workspace() {
  local workspace="$1"
  [[ -d "$workspace" ]] || fail "Workspace does not exist or is not a directory: $workspace"
}

build_codex_command() {
  local workspace="$1"
  local sandbox="$2"
  local model="$3"
  local approval_mode="$4"
  local ephemeral_enabled="$5"
  local json_enabled="$6"
  local prompt="$7"

  local -a cmd=(
    codex
    exec
    --cd "$workspace"
    --sandbox "$sandbox"
    --skip-git-repo-check
  )

  if [[ -n "$model" ]]; then
    cmd+=(--model "$model")
  fi

  if [[ -n "$approval_mode" ]]; then
    cmd+=(--config "approval_policy=\"$approval_mode\"")
  fi

  if [[ "$ephemeral_enabled" == "1" ]]; then
    cmd+=(--ephemeral)
  fi

  if [[ "$json_enabled" == "1" ]]; then
    cmd+=(--json)
  fi

  cmd+=("$prompt")
  printf '%s\0' "${cmd[@]}"
}

run_codex_prompt() {
  local workspace="$1"
  local sandbox="$2"
  local model="$3"
  local approval_mode="$4"
  local ephemeral_enabled="$5"
  local json_enabled="$6"
  local prompt="$7"

  local -a cmd=()
  while IFS= read -r -d '' part; do
    cmd+=("$part")
  done < <(build_codex_command "$workspace" "$sandbox" "$model" "$approval_mode" "$ephemeral_enabled" "$json_enabled" "$prompt")

  "${cmd[@]}" </dev/null
}

main() {
  local workspace="$DEFAULT_WORKSPACE"
  local sandbox="$DEFAULT_SANDBOX"
  local model="$DEFAULT_MODEL"
  local approval_mode="$DEFAULT_APPROVAL_MODE"
  local ephemeral_enabled="$DEFAULT_EPHEMERAL"
  local json_enabled="0"
  local prompt=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --prompt)
        [[ $# -ge 2 ]] || fail "--prompt requires a value"
        prompt="$2"
        shift 2
        ;;
      --workspace)
        [[ $# -ge 2 ]] || fail "--workspace requires a value"
        workspace="$2"
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
      --ephemeral)
        ephemeral_enabled="1"
        shift
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
        if [[ -z "$prompt" ]]; then
          prompt="$1"
          shift
        else
          fail "Unexpected extra argument: $1"
        fi
        ;;
    esac
  done

  [[ -n "$prompt" ]] || fail "A prompt is required. Use --prompt or pass it as the first positional argument."

  require_command codex
  validate_workspace "$workspace"
  run_codex_prompt "$workspace" "$sandbox" "$model" "$approval_mode" "$ephemeral_enabled" "$json_enabled" "$prompt"
}

main "$@"
