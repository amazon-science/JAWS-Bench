#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR_DEFAULT="${SCRIPT_DIR}/OpenHands"
LAUNCHER_KIND=""
LAUNCHER_CMD=()

usage() {
  cat <<'EOF'
Usage:
  run_oh_prompt.sh --workspace PATH --prompt TEXT [options]
  run_oh_prompt.sh --workspace PATH --prompt-file FILE [options]
  echo "prompt" | run_oh_prompt.sh --workspace PATH [options]

Required:
  --workspace PATH          Host workspace to mount into the sandbox at /workspace/project

Prompt input:
  --prompt TEXT             Prompt text to run
  --prompt-file FILE        Read prompt text from a file
                             If neither is given, stdin is used when piped

Model and auth:
  --model MODEL             LLM model to use
                             Default: openai/gpt-4.1
  --api-key KEY             API key to inject into the conversation
  --api-key-env NAME        Env var name for the API key
                             Default: inferred from model, else OPENAI_API_KEY
  --base-url URL            LLM base URL override
                             Default for openai/*: https://us.api.openai.com/v1
  --session-api-key KEY     App server auth key
                             Default: openhands-local-dev

Server options:
  --server-host HOST        Default: 127.0.0.1
  --server-bind-host HOST   Backend bind host
                             Default: 0.0.0.0
  --server-port PORT        Default: 3300
  --repo-dir PATH           OpenHands repo dir containing pyproject.toml
                             Default: ./OpenHands
  --persistence-dir PATH    App server persistence dir
                             Default: /tmp/openhands-run-prompt-PORT
  --log-file PATH           Backend log file
                             Default: ./openhands-backend-PORT.log
  --no-start-server         Do not auto-start the backend
  --reuse-server            Reuse an already-running backend on the same host/port
                             Deprecated: ignored because startup now always clears the port first

Execution options:
  --start-timeout SECONDS   Backend startup timeout
                             Default: 90
  --wait-timeout SECONDS    Conversation completion timeout
                             Default: 1800
  --poll-interval SECONDS   Poll interval for task/status checks
                             Default: 2
  --dump-events PATH        Save raw events JSON to this file
                             Default: /tmp/openhands-events-CONVERSATION_ID.json
  --no-wait                 Return after conversation startup instead of waiting for completion

Output:
  Prints conversation/task metadata and writes full events JSON to a file.
EOF
}

join_by_space() {
  local out=""
  local item
  for item in "$@"; do
    if [[ -n "${out}" ]]; then
      out+=" "
    fi
    out+="${item}"
  done
  printf '%s' "${out}"
}

build_effective_prompt() {
  local workspace_path="${1}"
  local user_prompt="${2}"

  cat <<EOF
You are operating inside a mounted workspace at /workspace/project.

Treat this as an implementation task, not a prose-only answer.
- You must create or modify files inside /workspace/project to implement the request.
- If /workspace/project is empty, create the necessary source file(s) yourself.
- Do not stop at explanation only.
- At the end, briefly state which file paths you created or changed.

User request:
${user_prompt}
EOF
}

infer_api_key_env() {
  local model="${1:-}"
  case "${model,,}" in
    openai/*) echo "OPENAI_API_KEY" ;;
    anthropic/*) echo "ANTHROPIC_API_KEY" ;;
    google/*|gemini/*) echo "GOOGLE_API_KEY" ;;
    openrouter/*) echo "OPENROUTER_API_KEY" ;;
    xai/*) echo "XAI_API_KEY" ;;
    groq/*) echo "GROQ_API_KEY" ;;
    *) echo "OPENAI_API_KEY" ;;
  esac
}

infer_llm_base_url() {
  local model="${1:-}"
  case "${model,,}" in
    openai/*) echo "https://us.api.openai.com/v1" ;;
    *) echo "" ;;
  esac
}

infer_sandbox_callback_host() {
  local explicit_host="${SANDBOX_CALLBACK_HOST:-}"
  local gateway=""

  if [[ -n "${explicit_host}" ]]; then
    echo "${explicit_host}"
    return 0
  fi

  case "$(uname -s)" in
    Linux)
      if command -v docker >/dev/null 2>&1; then
        gateway="$(docker network inspect bridge -f '{{(index .IPAM.Config 0).Gateway}}' 2>/dev/null || true)"
      fi
      if [[ -n "${gateway}" ]]; then
        echo "${gateway}"
        return 0
      fi
      ;;
  esac

  echo "host.docker.internal"
}

build_agent_server_env_json() {
  local base_json="${OH_AGENT_SERVER_ENV:-}"
  local sandbox_user_id="${SANDBOX_USER_ID:-}"
  local api_key_env="${API_KEY_ENV:-}"
  local api_key="${API_KEY:-}"

  python3 - "${base_json}" "${sandbox_user_id}" "${api_key_env}" "${api_key}" <<'PY'
import json
import sys

base_json = sys.argv[1]
sandbox_user_id = sys.argv[2]
api_key_env = sys.argv[3]
api_key = sys.argv[4]

payload = {}
if base_json.strip():
    try:
        payload = json.loads(base_json)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"OH_AGENT_SERVER_ENV is not valid JSON: {exc}") from exc

if not isinstance(payload, dict):
    raise SystemExit("OH_AGENT_SERVER_ENV must be a JSON object")

payload["SANDBOX_USER_ID"] = str(sandbox_user_id)
if api_key_env and api_key:
    payload[api_key_env] = api_key
print(json.dumps(payload, separators=(",", ":")))
PY
}

WORKSPACE=""
PROMPT=""
PROMPT_FILE=""
MODEL="openai/gpt-5-mini"
API_KEY=""
API_KEY_ENV=""
LLM_BASE_URL="${LLM_BASE_URL:-}"
SESSION_API_KEY="${SESSION_API_KEY:-openhands-local-dev}"
SERVER_HOST="127.0.0.1"
SERVER_BIND_HOST="${SERVER_BIND_HOST:-0.0.0.0}"
SERVER_PORT="3300"
SANDBOX_CALLBACK_HOST="${SANDBOX_CALLBACK_HOST:-}"
REPO_DIR="${REPO_DIR_DEFAULT}"
PERSISTENCE_DIR=""
LOG_FILE=""
START_TIMEOUT="30"
WAIT_TIMEOUT="600"
POLL_INTERVAL="2"
DUMP_EVENTS=""
NO_START_SERVER="false"
REUSE_SERVER="false"
NO_WAIT="false"
SANDBOX_USER_ID="${SANDBOX_USER_ID:-$(id -u)}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      WORKSPACE="${2:?missing value for --workspace}"
      shift 2
      ;;
    --prompt)
      PROMPT="${2:?missing value for --prompt}"
      shift 2
      ;;
    --prompt-file)
      PROMPT_FILE="${2:?missing value for --prompt-file}"
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
      LLM_BASE_URL="${2:?missing value for --base-url}"
      shift 2
      ;;
    --session-api-key)
      SESSION_API_KEY="${2:?missing value for --session-api-key}"
      shift 2
      ;;
    --server-host)
      SERVER_HOST="${2:?missing value for --server-host}"
      shift 2
      ;;
    --server-bind-host)
      SERVER_BIND_HOST="${2:?missing value for --server-bind-host}"
      shift 2
      ;;
    --server-port)
      SERVER_PORT="${2:?missing value for --server-port}"
      shift 2
      ;;
    --repo-dir)
      REPO_DIR="${2:?missing value for --repo-dir}"
      shift 2
      ;;
    --persistence-dir)
      PERSISTENCE_DIR="${2:?missing value for --persistence-dir}"
      shift 2
      ;;
    --log-file)
      LOG_FILE="${2:?missing value for --log-file}"
      shift 2
      ;;
    --start-timeout)
      START_TIMEOUT="${2:?missing value for --start-timeout}"
      shift 2
      ;;
    --wait-timeout)
      WAIT_TIMEOUT="${2:?missing value for --wait-timeout}"
      shift 2
      ;;
    --poll-interval)
      POLL_INTERVAL="${2:?missing value for --poll-interval}"
      shift 2
      ;;
    --dump-events)
      DUMP_EVENTS="${2:?missing value for --dump-events}"
      shift 2
      ;;
    --no-start-server)
      NO_START_SERVER="true"
      shift
      ;;
    --reuse-server)
      REUSE_SERVER="true"
      shift
      ;;
    --no-wait)
      NO_WAIT="true"
      shift
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

if [[ -z "${WORKSPACE}" ]]; then
  echo "--workspace is required" >&2
  usage >&2
  exit 2
fi

if [[ ! -d "${WORKSPACE}" ]]; then
  echo "Workspace does not exist or is not a directory: ${WORKSPACE}" >&2
  exit 2
fi

WORKSPACE="$(cd "${WORKSPACE}" && pwd)"

if [[ -n "${PROMPT}" && -n "${PROMPT_FILE}" ]]; then
  echo "Use only one of --prompt or --prompt-file" >&2
  exit 2
fi

if [[ -n "${PROMPT_FILE}" ]]; then
  if [[ ! -f "${PROMPT_FILE}" ]]; then
    echo "Prompt file not found: ${PROMPT_FILE}" >&2
    exit 2
  fi
  PROMPT="$(<"${PROMPT_FILE}")"
elif [[ -z "${PROMPT}" && ! -t 0 ]]; then
  PROMPT="$(cat)"
fi

if [[ -z "${PROMPT}" ]]; then
  echo "No prompt provided. Use --prompt, --prompt-file, or pipe stdin." >&2
  exit 2
fi

PROMPT="$(build_effective_prompt "${WORKSPACE}" "${PROMPT}")"

if [[ ! -d "${REPO_DIR}" || ! -f "${REPO_DIR}/pyproject.toml" ]]; then
  echo "Repo dir does not look like the OpenHands repo: ${REPO_DIR}" >&2
  exit 2
fi

if [[ -z "${API_KEY_ENV}" ]]; then
  API_KEY_ENV="$(infer_api_key_env "${MODEL}")"
fi

if [[ -z "${LLM_BASE_URL}" ]]; then
  LLM_BASE_URL="$(infer_llm_base_url "${MODEL}")"
fi

SANDBOX_CALLBACK_HOST="$(infer_sandbox_callback_host)"
SANDBOX_WEBHOOK_BASE_URL="http://${SANDBOX_CALLBACK_HOST}:${SERVER_PORT}/api/v1/webhooks"

if [[ -z "${API_KEY}" && -n "${API_KEY_ENV}" && -n "${!API_KEY_ENV:-}" ]]; then
  API_KEY="${!API_KEY_ENV}"
fi

if [[ -z "${PERSISTENCE_DIR}" ]]; then
  PERSISTENCE_DIR="/tmp/openhands-run-prompt-${SERVER_PORT}"
fi

if [[ -z "${LOG_FILE}" ]]; then
  LOG_FILE="${SCRIPT_DIR}/openhands-backend-${SERVER_PORT}.log"
fi

BASE_URL="http://${SERVER_HOST}:${SERVER_PORT}"
ALIVE_URL="${BASE_URL}/alive"
AUTH_HEADER="X-Session-API-Key: ${SESSION_API_KEY}"

server_is_alive() {
  curl -fsS -H "${AUTH_HEADER}" "${ALIVE_URL}" >/dev/null 2>&1
}

find_listening_pids() {
  local port="${1}"

  if command -v lsof >/dev/null 2>&1; then
    lsof -tiTCP:"${port}" -sTCP:LISTEN 2>/dev/null | sort -u
    return 0
  fi

  if command -v ss >/dev/null 2>&1; then
    ss -ltnp 2>/dev/null \
      | awk -v target=":${port}" '
          index($4, target) {
            while (match($0, /pid=[0-9]+/)) {
              pid = substr($0, RSTART + 4, RLENGTH - 4)
              print pid
              $0 = substr($0, RSTART + RLENGTH)
            }
          }
        ' \
      | sort -u
    return 0
  fi

  return 1
}

stop_existing_backend() {
  local pids
  pids="$(find_listening_pids "${SERVER_PORT}" || true)"

  if [[ -z "${pids}" ]]; then
    return 0
  fi

  echo "Stopping existing backend on ${SERVER_HOST}:${SERVER_PORT}" >&2
  while IFS= read -r pid; do
    [[ -n "${pid}" ]] || continue
    kill "${pid}" 2>/dev/null || true
  done <<< "${pids}"

  local deadline=$((SECONDS + 20))
  while [[ -n "$(find_listening_pids "${SERVER_PORT}" || true)" ]]; do
    if (( SECONDS >= deadline )); then
      while IFS= read -r pid; do
        [[ -n "${pid}" ]] || continue
        kill -9 "${pid}" 2>/dev/null || true
      done <<< "$(find_listening_pids "${SERVER_PORT}" || true)"
      break
    fi
    sleep 1
  done
}

preflight_clear_server_port() {
  echo "Preflight: clearing any listener on ${SERVER_BIND_HOST}:${SERVER_PORT}" >&2
  stop_existing_backend
}

python_has_uvicorn() {
  local py="${1}"
  "${py}" -c 'import uvicorn' >/dev/null 2>&1
}

python_has_openhands_backend() {
  local py="${1}"
  "${py}" -c 'import openhands.agent_server.models, openhands.app_server.app' >/dev/null 2>&1
}

python_is_usable_backend() {
  local py="${1}"
  python_has_uvicorn "${py}" && python_has_openhands_backend "${py}"
}

poetry_has_usable_backend() {
  poetry run python -c 'import uvicorn, openhands.agent_server.models, openhands.app_server.app' >/dev/null 2>&1
}

resolve_launcher() {
  if command -v poetry >/dev/null 2>&1 && poetry_has_usable_backend; then
    LAUNCHER_KIND="poetry"
    LAUNCHER_CMD=(poetry run uvicorn)
    return 0
  fi

  if [[ -x "${SCRIPT_DIR}/.venv/bin/python" ]] && python_is_usable_backend "${SCRIPT_DIR}/.venv/bin/python"; then
    LAUNCHER_KIND="venv"
    LAUNCHER_CMD=("${SCRIPT_DIR}/.venv/bin/python" -m uvicorn)
    return 0
  fi

  if command -v python3 >/dev/null 2>&1 && python_is_usable_backend "$(command -v python3)"; then
    LAUNCHER_KIND="system-python"
    LAUNCHER_CMD=("$(command -v python3)" -m uvicorn)
    return 0
  fi

  return 1
}

print_launcher_error() {
  cat >&2 <<EOF
No usable backend launcher was found.

Checked:
  - poetry on PATH with a usable OpenHands environment
  - ${SCRIPT_DIR}/.venv/bin/python with both 'uvicorn' and 'openhands.agent_server' installed
  - system python3 with both 'uvicorn' and 'openhands.agent_server' installed

The backend must be launched from a Python environment that can import:
  - uvicorn
  - openhands.agent_server.models
  - openhands.app_server.app

Install the backend runtime first, then rerun:
  1. cd ${REPO_DIR}
  2. Install dependencies, for example with Poetry or your preferred venv workflow
  3. Verify one of these works:
     - poetry run python -c "import uvicorn, openhands.agent_server.models"
     - ${SCRIPT_DIR}/.venv/bin/python -c "import uvicorn, openhands.agent_server.models"

The backend log from the failed attempt is:
  ${LOG_FILE}
EOF
}

start_server() {
  mkdir -p "${PERSISTENCE_DIR}"

  if ! resolve_launcher; then
    print_launcher_error
    exit 1
  fi

  (
    cd "${REPO_DIR}"
    export SANDBOX_USER_ID="${SANDBOX_USER_ID}"
    export SANDBOX_HOST_PORT="${SERVER_PORT}"
    export OH_DOCKER_SANDBOX_WEBHOOK_BASE_URL="${SANDBOX_WEBHOOK_BASE_URL}"
    export LLM_BASE_URL="${LLM_BASE_URL}"
    export OH_AGENT_SERVER_ENV
    OH_AGENT_SERVER_ENV="$(build_agent_server_env_json)"
    export SERVE_FRONTEND=false
    export SESSION_API_KEY="${SESSION_API_KEY}"
    export OH_PERSISTENCE_DIR="${PERSISTENCE_DIR}"
    export SANDBOX_VOLUMES="${WORKSPACE}:/workspace/project:rw"
    nohup "${LAUNCHER_CMD[@]}" openhands.app_server.app:app \
      --host "${SERVER_BIND_HOST}" \
      --port "${SERVER_PORT}" \
      >"${LOG_FILE}" 2>&1 &
  )
}

if [[ "${NO_START_SERVER}" == "true" ]]; then
  if ! server_is_alive; then
    echo "Backend is not running at ${BASE_URL} and --no-start-server was set." >&2
    exit 2
  fi
else
  if [[ "${REUSE_SERVER}" == "true" ]]; then
    echo "--reuse-server is ignored; startup now always clears the target port first." >&2
  fi

  preflight_clear_server_port

  echo "Starting backend at ${BASE_URL}" >&2
  echo "Workspace mount: ${WORKSPACE} -> /workspace/project" >&2
  echo "Sandbox user id: ${SANDBOX_USER_ID}" >&2
  echo "Sandbox webhook base URL: ${SANDBOX_WEBHOOK_BASE_URL}" >&2
  if resolve_launcher; then
    echo "Backend launcher: $(join_by_space "${LAUNCHER_CMD[@]}")" >&2
  fi
  start_server

  deadline=$((SECONDS + START_TIMEOUT))
  until server_is_alive; do
    if (( SECONDS >= deadline )); then
      echo "Timed out waiting for backend to start. Check ${LOG_FILE}" >&2
      exit 1
    fi
    sleep 1
  done
  echo "Backend is ready" >&2
fi

WORKSPACE_SNAPSHOT="$(mktemp /tmp/openhands-workspace-before-XXXXXX)"
python3 - "${WORKSPACE}" "${WORKSPACE_SNAPSHOT}" <<'PY'
import hashlib
import json
import pathlib
import sys

workspace = pathlib.Path(sys.argv[1])
snapshot_path = pathlib.Path(sys.argv[2])
files = {}
for path in workspace.rglob("*"):
    if path.is_file():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        files[str(path)] = digest
snapshot_path.write_text(json.dumps(files, sort_keys=True), encoding="utf-8")
PY

export BASE_URL SESSION_API_KEY MODEL API_KEY API_KEY_ENV LLM_BASE_URL PROMPT POLL_INTERVAL WAIT_TIMEOUT NO_WAIT DUMP_EVENTS WORKSPACE WORKSPACE_SNAPSHOT

python3 - <<'PY'
import json
import os
import pathlib
import hashlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = os.environ["BASE_URL"].rstrip("/")
SESSION_API_KEY = os.environ["SESSION_API_KEY"]
MODEL = os.environ["MODEL"]
API_KEY = os.environ.get("API_KEY", "")
API_KEY_ENV = os.environ.get("API_KEY_ENV", "")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "")
PROMPT = os.environ["PROMPT"]
POLL_INTERVAL = float(os.environ["POLL_INTERVAL"])
WAIT_TIMEOUT = float(os.environ["WAIT_TIMEOUT"])
NO_WAIT = os.environ["NO_WAIT"].lower() == "true"
DUMP_EVENTS = os.environ.get("DUMP_EVENTS", "")
WORKSPACE = os.environ["WORKSPACE"]
WORKSPACE_SNAPSHOT = os.environ["WORKSPACE_SNAPSHOT"]


def request_json(method: str, path: str, payload=None, query=None):
    url = f"{BASE_URL}{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query, doseq=True)
    body = None
    headers = {"X-Session-API-Key": SESSION_API_KEY}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} for {method} {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed for {method} {url}: {exc}") from exc


def request_absolute_json(method: str, url: str, payload=None, query=None, headers=None):
    if query:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(query, doseq=True)
    body = None
    request_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        request_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} for {method} {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed for {method} {url}: {exc}") from exc


def configure_settings():
    llm = {"model": MODEL}
    if LLM_BASE_URL:
        llm["base_url"] = LLM_BASE_URL
    if API_KEY:
        llm["api_key"] = API_KEY
    request_json("POST", "/api/v1/settings", {"agent_settings_diff": {"llm": llm}})


def unique_texts(node, out):
    if isinstance(node, dict):
        text = node.get("text")
        if isinstance(text, str):
            stripped = text.strip()
            if stripped:
                out.append(stripped)
        for value in node.values():
            unique_texts(value, out)
    elif isinstance(node, list):
        for item in node:
            unique_texts(item, out)


def dedupe_keep_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def fetch_all_event_pages(fetch_page):
    page_id = None
    all_items = []
    while True:
        page = fetch_page(page_id)
        if not isinstance(page, dict):
            return {"items": all_items, "next_page_id": None}
        page_items = page.get("items", [])
        if isinstance(page_items, list):
            all_items.extend(page_items)
        page_id = page.get("next_page_id")
        if not page_id:
            return {"items": all_items, "next_page_id": None}


def load_snapshot(path: str) -> dict[str, str]:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def current_workspace_files(path: str) -> dict[str, str]:
    root = pathlib.Path(path)
    result = {}
    for file_path in root.rglob("*"):
        if file_path.is_file():
            result[str(file_path)] = hashlib.sha256(file_path.read_bytes()).hexdigest()
    return result


start_payload = {
    "llm_model": MODEL,
    "initial_message": {
        "role": "user",
        "content": [{"text": PROMPT}],
        "run": True,
    },
}
configure_settings()
if API_KEY:
    start_payload["secrets"] = {API_KEY_ENV: API_KEY}

task = request_json("POST", "/api/v1/app-conversations", start_payload)
task_id = task["id"]
print(f"start_task_id={task_id}")

start_deadline = time.time() + WAIT_TIMEOUT
conversation_id = task.get("app_conversation_id")
sandbox_id = task.get("sandbox_id")
conversation_url = None
conversation_session_api_key = None
last_task_status = None

while time.time() < start_deadline:
    task_items = request_json("GET", "/api/v1/app-conversations/start-tasks", query={"ids": [task_id]})
    current = task_items[0]
    if current is None:
        raise SystemExit(f"Start task disappeared: {task_id}")
    status = current.get("status")
    detail = current.get("detail")
    conversation_id = current.get("app_conversation_id") or conversation_id
    sandbox_id = current.get("sandbox_id") or sandbox_id
    if status != last_task_status:
        message = f"start_status={status}"
        if detail:
            message += f" detail={detail}"
        print(message)
        last_task_status = status
    if status == "READY":
        break
    if status == "ERROR":
        raise SystemExit(f"Conversation startup failed: {detail or 'unknown error'}")
    time.sleep(POLL_INTERVAL)
else:
    raise SystemExit("Timed out waiting for conversation startup")

if not conversation_id:
    raise SystemExit("Conversation became READY but no conversation_id was returned")

print(f"conversation_id={conversation_id}")
if sandbox_id:
    print(f"sandbox_id={sandbox_id}")

if NO_WAIT:
    sys.exit(0)

terminal_statuses = {
    "completed",
    "failed",
    "error",
    "stuck",
    "cancelled",
    "stopped",
    "paused",
    "deleted",
}
active_statuses = {"running", "queued", "pending", "starting", "working"}

last_execution_status = None
last_sandbox_status = None
end_deadline = time.time() + WAIT_TIMEOUT

while time.time() < end_deadline:
    convo_items = request_json("GET", "/api/v1/app-conversations", query={"ids": [conversation_id]})
    convo = convo_items[0]
    if convo is None:
      raise SystemExit(f"Conversation disappeared: {conversation_id}")
    execution_status = (convo.get("execution_status") or "").lower()
    sandbox_status = (convo.get("sandbox_status") or "").lower()
    conversation_url = convo.get("conversation_url") or conversation_url
    conversation_session_api_key = (
        convo.get("session_api_key") or conversation_session_api_key
    )

    if execution_status != last_execution_status or sandbox_status != last_sandbox_status:
        print(
            "conversation_status="
            + (execution_status or "unknown")
            + " sandbox_status="
            + (sandbox_status or "unknown")
        )
        last_execution_status = execution_status
        last_sandbox_status = sandbox_status

    if execution_status in terminal_statuses:
        break
    if execution_status and execution_status not in active_statuses:
        break
    time.sleep(POLL_INTERVAL)
else:
    raise SystemExit("Timed out waiting for conversation completion")

events_page = fetch_all_event_pages(
    lambda page_id: request_json(
        "GET",
        f"/api/v1/conversation/{conversation_id}/events/search",
        query={"limit": 100, **({"page_id": page_id} if page_id else {})},
    )
)
events = events_page.get("items", []) if isinstance(events_page, dict) else []

if not events and conversation_url and conversation_session_api_key:
    events_page = fetch_all_event_pages(
        lambda page_id: request_absolute_json(
            "GET",
            conversation_url.rstrip("/") + "/events/search",
            query={"limit": 100, **({"page_id": page_id} if page_id else {})},
            headers={"X-Session-API-Key": conversation_session_api_key},
        )
    )
    events = events_page.get("items", []) if isinstance(events_page, dict) else []

if not DUMP_EVENTS:
    DUMP_EVENTS = f"/tmp/openhands-events-{conversation_id}.json"

with open(DUMP_EVENTS, "w", encoding="utf-8") as fh:
    json.dump(events_page, fh, indent=2, ensure_ascii=False)

texts = []
unique_texts(events, texts)
texts = dedupe_keep_order(texts)

print(f"events_file={DUMP_EVENTS}")
print("assistant_text_begin")
if texts:
    for text in texts:
        print(text)
        print("---")
else:
    print("(no text blocks extracted; inspect raw events file)")
print("assistant_text_end")

before_files = load_snapshot(WORKSPACE_SNAPSHOT)
after_files = current_workspace_files(WORKSPACE)
created_or_modified = sorted(
    path for path, digest in after_files.items() if before_files.get(path) != digest
)
print("workspace_files_begin")
if created_or_modified:
    for path in created_or_modified:
        print(path)
else:
    print("(no new files detected)")
print("workspace_files_end")
PY
