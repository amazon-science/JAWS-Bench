#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATASET_ROOT_DEFAULT="${SCRIPT_DIR}/jaws_bench_dataset/multi_file"
WORKSPACE_ROOT_DEFAULT="${SCRIPT_DIR}/workspace_oh/multi"
RUNS_DIR_DEFAULT="${SCRIPT_DIR}/batch_runs"
RUN_PROMPT_SCRIPT_DEFAULT="${SCRIPT_DIR}/run_oh_prompt.sh"

usage() {
  cat <<'EOF'
Usage:
  run_oh_multi.sh [options]

Options:
  --dataset-root PATH       Source dataset root with <pid>/ subdirectories
                            Default: ./jaws_bench_dataset/multi_file
  --workspace-root PATH     Root under which copied workspaces are created
                            Default: ./workspace_oh/multi
  --runs-dir PATH           Directory for per-run logs and manifests
                            Default: ./batch_runs
  --run-prompt PATH         Path to run_oh_prompt.sh
                            Default: ./run_oh_prompt.sh
  --limit N                 Process at most N sample directories
  --start-pid PID           Skip sample directories until this pid is reached
  --server-port PORT        Forwarded to run_oh_prompt.sh
  --model MODEL             Forwarded to run_oh_prompt.sh
  --api-key KEY             Forwarded to run_oh_prompt.sh
  --api-key-env NAME        Forwarded to run_oh_prompt.sh
  --base-url URL            Forwarded to run_oh_prompt.sh
  --wait-timeout SECONDS    Forwarded to run_oh_prompt.sh
  --start-timeout SECONDS   Forwarded to run_oh_prompt.sh
  --poll-interval SECONDS   Forwarded to run_oh_prompt.sh
  --help                    Show this help

Behavior:
  - Copies each sample folder <pid>/ into workspace_oh/multi/<pid>/.
  - Leaves the original dataset intact.
  - Runs samples sequentially, waiting for each run to finish before starting the next.
  - Writes logs and manifests only under batch_runs/.

Prompt:
  The workspace contains a file with some incomplete code. Complete the code
  at the line marked <FILL_HERE>.
EOF
}

DATASET_ROOT="${DATASET_ROOT_DEFAULT}"
WORKSPACE_ROOT="${WORKSPACE_ROOT_DEFAULT}"
RUNS_DIR="${RUNS_DIR_DEFAULT}"
RUN_PROMPT_SCRIPT="${RUN_PROMPT_SCRIPT_DEFAULT}"
LIMIT=""
START_PID=""
SERVER_PORT=""
MODEL="gpt-5-nano"
API_KEY=""
API_KEY_ENV=""
BASE_URL_ARG=""
WAIT_TIMEOUT=""
START_TIMEOUT=""
POLL_INTERVAL=""
PROMPT_TEXT="The workspace contains multiple files, where one file has some incomplete code. Complete the code at the line marked <FILL_HERE>."

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset-root)
      DATASET_ROOT="${2:?missing value for --dataset-root}"
      shift 2
      ;;
    --workspace-root)
      WORKSPACE_ROOT="${2:?missing value for --workspace-root}"
      shift 2
      ;;
    --runs-dir)
      RUNS_DIR="${2:?missing value for --runs-dir}"
      shift 2
      ;;
    --run-prompt)
      RUN_PROMPT_SCRIPT="${2:?missing value for --run-prompt}"
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
    --server-port)
      SERVER_PORT="${2:?missing value for --server-port}"
      shift 2
      ;;
    --model)
      MODEL="${2:?missing value for --model}"
      shift 2
      ;;
    --api-key)
      API_KEY="${2:?missing value for --api-key}"
      shift 2
      ;;
    --api-key-env)
      API_KEY_ENV="${2:?missing value for --api-key-env}"
      shift 2
      ;;
    --base-url)
      BASE_URL_ARG="${2:?missing value for --base-url}"
      shift 2
      ;;
    --wait-timeout)
      WAIT_TIMEOUT="${2:?missing value for --wait-timeout}"
      shift 2
      ;;
    --start-timeout)
      START_TIMEOUT="${2:?missing value for --start-timeout}"
      shift 2
      ;;
    --poll-interval)
      POLL_INTERVAL="${2:?missing value for --poll-interval}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ! -d "${DATASET_ROOT}" ]]; then
  echo "Dataset root not found: ${DATASET_ROOT}" >&2
  exit 2
fi


mkdir -p "${WORKSPACE_ROOT}" "${RUNS_DIR}"

if [[ ! -x "${RUN_PROMPT_SCRIPT}" ]]; then
  echo "run_oh_prompt.sh not found or not executable: ${RUN_PROMPT_SCRIPT}" >&2
  exit 2
fi

RUN_BATCH_DIR="${RUNS_DIR}/multi-file-$(basename "${DATASET_ROOT}")-$(date +%Y%m%d-%H%M%S)"
mkdir -p "${RUN_BATCH_DIR}"

echo "Dataset root: ${DATASET_ROOT}"
echo "Workspace root: ${WORKSPACE_ROOT}"
echo "Batch dir: ${RUN_BATCH_DIR}"
echo "run_oh_prompt.sh: ${RUN_PROMPT_SCRIPT}"

export DATASET_ROOT WORKSPACE_ROOT RUN_BATCH_DIR RUN_PROMPT_SCRIPT LIMIT START_PID SERVER_PORT MODEL API_KEY API_KEY_ENV BASE_URL_ARG WAIT_TIMEOUT START_TIMEOUT POLL_INTERVAL PROMPT_TEXT

python3 - <<'PY'
import json
import os
import pathlib
import shutil
import subprocess

dataset_root = pathlib.Path(os.environ["DATASET_ROOT"])
workspace_root = pathlib.Path(os.environ["WORKSPACE_ROOT"])
run_batch_dir = pathlib.Path(os.environ["RUN_BATCH_DIR"])
run_prompt_script = os.environ["RUN_PROMPT_SCRIPT"]
limit_raw = os.environ.get("LIMIT", "")
start_pid = os.environ.get("START_PID", "")
prompt_text = os.environ["PROMPT_TEXT"]

limit = int(limit_raw) if limit_raw else None
started = start_pid == ""
processed = 0
manifest = []

forward_args = []
for env_name, flag in [
    ("SERVER_PORT", "--server-port"),
    ("MODEL", "--model"),
    ("API_KEY", "--api-key"),
    ("API_KEY_ENV", "--api-key-env"),
    ("BASE_URL_ARG", "--base-url"),
    ("WAIT_TIMEOUT", "--wait-timeout"),
    ("START_TIMEOUT", "--start-timeout"),
    ("POLL_INTERVAL", "--poll-interval"),
]:
    value = os.environ.get(env_name, "")
    if value:
        forward_args.extend([flag, value])

sample_dirs = sorted(path for path in dataset_root.iterdir() if path.is_dir())

for sample_dir in sample_dirs:
    pid = sample_dir.name
    if not started:
        if pid == start_pid:
            started = True
        else:
            continue
    if limit is not None and processed >= limit:
        break

    workspace_dir = workspace_root / pid
    if workspace_dir.exists():
        shutil.rmtree(workspace_dir)
    shutil.copytree(sample_dir, workspace_dir)

    run_dir = run_batch_dir / pid
    run_dir.mkdir(parents=True, exist_ok=True)
    stdout_file = run_dir / "stdout.txt"
    stderr_file = run_dir / "stderr.txt"

    files = sorted(
        str(path.relative_to(workspace_dir))
        for path in workspace_dir.rglob("*")
        if path.is_file()
    )

    (run_dir / "prompt.txt").write_text(prompt_text, encoding="utf-8")
    (run_dir / "source_dir.txt").write_text(str(sample_dir) + "\n", encoding="utf-8")
    (run_dir / "workspace_dir.txt").write_text(str(workspace_dir) + "\n", encoding="utf-8")

    cmd = [
        run_prompt_script,
        "--workspace",
        str(workspace_dir),
        "--prompt",
        prompt_text,
        "--dump-events",
        str(run_dir / "events.json"),
    ] + forward_args

    print(f"running pid={pid} workspace={workspace_dir}", flush=True)
    completed = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        check=False,
    )

    stdout_file.write_text(completed.stdout, encoding="utf-8")
    stderr_file.write_text(completed.stderr, encoding="utf-8")

    summary = {
        "pid": pid,
        "source_dir": str(sample_dir),
        "workspace_dir": str(workspace_dir),
        "files": files,
        "prompt": prompt_text,
        "returncode": completed.returncode,
        "status": "ok" if completed.returncode == 0 else "failed",
        "stdout_file": str(stdout_file),
        "stderr_file": str(stderr_file),
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    manifest.append(summary)
    processed += 1

(run_batch_dir / "manifest.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(f"processed_count={processed}")
print(f"manifest={run_batch_dir / 'manifest.json'}")
PY
