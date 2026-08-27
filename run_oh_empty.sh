#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATASET_DIR_DEFAULT="${SCRIPT_DIR}/jaws_bench_dataset/empty"
WORKSPACE_ROOT_DEFAULT="${SCRIPT_DIR}/workspace_oh/empty"
RUN_PROMPT_SCRIPT_DEFAULT="${SCRIPT_DIR}/run_oh_prompt.sh"
RUNS_DIR_DEFAULT="${SCRIPT_DIR}/batch_runs"

usage() {
  cat <<'EOF'
Usage:
  run_oh_empty.sh [options]

Options:
  --csv PATH                CSV file with at least pid,prompt columns
                            Default: ./jaws_bench_dataset/empty/t2c_l1.csv
  --dataset-dir PATH        Dataset empty dir
                            Default: ./jaws_bench_dataset/empty
  --workspace-root PATH     Root under which per-pid workspaces are created
                            Default: ./workspace_oh/empty
  --runs-dir PATH           Directory for per-run logs and manifests
                            Default: ./batch_runs
  --run-prompt PATH         Path to run_oh_prompt.sh
                            Default: ./run_oh_prompt.sh
  --limit N                 Process at most N rows
  --start-pid PID           Skip rows until this pid is reached
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
  - Creates a fresh workspace directory at workspace_oh/empty/<pid>/ for each CSV row.
  - Runs rows sequentially, waiting for each run to finish before starting the next.
  - Stores prompt text, raw stdout/stderr, and a manifest under batch_runs/.

EOF
}

CSV_PATH="${DATASET_DIR_DEFAULT}/t2c_l1.csv"
DATASET_DIR="${DATASET_DIR_DEFAULT}"
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

while [[ $# -gt 0 ]]; do
  case "$1" in
    --csv)
      CSV_PATH="${2:?missing value for --csv}"
      shift 2
      ;;
    --dataset-dir)
      DATASET_DIR="${2:?missing value for --dataset-dir}"
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

if [[ ! -d "${DATASET_DIR}" ]]; then
  echo "Dataset dir not found: ${DATASET_DIR}" >&2
  exit 2
fi

if [[ ! -f "${CSV_PATH}" ]]; then
  echo "CSV file not found: ${CSV_PATH}" >&2
  exit 2
fi


mkdir -p "${WORKSPACE_ROOT}" "${RUNS_DIR}"

if [[ ! -x "${RUN_PROMPT_SCRIPT}" ]]; then
  echo "run_oh_prompt.sh not found or not executable: ${RUN_PROMPT_SCRIPT}" >&2
  exit 2
fi

RUN_BATCH_DIR="${RUNS_DIR}/$(basename "${CSV_PATH}" .csv)-$(date +%Y%m%d-%H%M%S)"
mkdir -p "${RUN_BATCH_DIR}"

echo "Batch dir: ${RUN_BATCH_DIR}"
echo "CSV: ${CSV_PATH}"
echo "Workspace root: ${WORKSPACE_ROOT}"
echo "run_oh_prompt.sh: ${RUN_PROMPT_SCRIPT}"

export RUN_PROMPT_SCRIPT WORKSPACE_ROOT RUN_BATCH_DIR SERVER_PORT MODEL API_KEY API_KEY_ENV BASE_URL_ARG WAIT_TIMEOUT START_TIMEOUT POLL_INTERVAL

python3 - "${CSV_PATH}" "${LIMIT}" "${START_PID}" <<'PY'
import csv
import json
import os
import pathlib
import subprocess
import sys

csv_path = pathlib.Path(sys.argv[1])
limit_raw = sys.argv[2]
start_pid = sys.argv[3]

run_prompt_script = os.environ["RUN_PROMPT_SCRIPT"]
workspace_root = pathlib.Path(os.environ["WORKSPACE_ROOT"])
run_batch_dir = pathlib.Path(os.environ["RUN_BATCH_DIR"])

limit = int(limit_raw) if limit_raw else None
started = start_pid == ""
processed = 0
manifest: list[dict] = []

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

with csv_path.open(newline="", encoding="utf-8") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        pid = (row.get("pid") or "").strip()
        prompt = row.get("prompt") or ""
        if not pid or not prompt.strip():
            continue
        if not started:
            if pid == start_pid:
                started = True
            else:
                continue
        if limit is not None and processed >= limit:
            break

        workspace_dir = workspace_root / pid
        workspace_dir.mkdir(parents=True, exist_ok=True)

        run_dir = run_batch_dir / pid
        run_dir.mkdir(parents=True, exist_ok=True)
        stdout_file = run_dir / "stdout.txt"
        stderr_file = run_dir / "stderr.txt"
        prompt_file = run_dir / "prompt.txt"
        row_file = run_dir / "row.json"

        prompt_file.write_text(prompt, encoding="utf-8")
        row_file.write_text(
            json.dumps(row, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        cmd = [
            run_prompt_script,
            "--workspace",
            str(workspace_dir),
            "--prompt",
            prompt,
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

        status = "ok" if completed.returncode == 0 else "failed"
        summary = {
            "pid": pid,
            "workspace": str(workspace_dir),
            "prompt_file": str(prompt_file),
            "stdout_file": str(stdout_file),
            "stderr_file": str(stderr_file),
            "returncode": completed.returncode,
            "status": status,
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
