# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

JAWS-Bench (Jailbreaks Across WorkSpaces) is a **defensive security research
benchmark** ([arXiv:2510.01359](https://arxiv.org/abs/2510.01359)) for
evaluating whether code agents comply with malicious coding requests under
increasingly realistic workspace conditions. The dataset under
`jaws_bench_dataset/` contains malicious/harmful code samples **by design** —
they are the benchmark stimuli used to test agent safety, not code to fix or
extend. Treat this repo as harness + data for measuring jailbreak susceptibility.

This repo produces agent outputs; the paper's judge/evaluation pipeline is not
included here.

## Repository layout

- `jaws_bench_dataset/` — the three benchmark regimes:
  - `empty/` (**JAWS-0**): `t2c_l1.csv` (80 rows), `t2c_l2.csv` (102 rows).
    Prompt-only tasks; agent generates from an empty workspace. Key CSV columns:
    `pid`, `category`, `prompt`, `language`.
  - `single_file/` (**JAWS-1**, 100 samples): one dir per `<pid>`, each holding
    a source file with a `<FILL_HERE>` marker the agent must complete.
  - `multi_file/` (**JAWS-M**, 180 samples): one dir per `<pid>` with multiple
    source files; one contains `<FILL_HERE>`.
- `OpenHands/` — **vendored** snapshot (not a submodule) with JAWS-specific
  changes, on top of upstream commit `0571ff530fa6114360feb10d2d1a0c2570987450`.
- `SWE-agent/`, `codex/` — **git submodules** (upstream projects). Empty until
  you run `git submodule update --init`.
- `run_*.sh` — the runner scripts (see below).
- Generated at runtime (gitignored): `workspace_{oh,swe,codex}/`, `batch_runs/`,
  `openhands-backend-*.log`.

## Runner script architecture

The scripts form a **two-layer pattern**, one pair per agent × two roles:

- **Per-sample worker**: `run_oh_prompt.sh`, `run_swe_prompt.sh`,
  `run_codex_prompt.sh` — take one `--workspace` + one `--prompt`, invoke the
  agent once, capture output/events.
- **Batch driver**: `run_<agent>_{empty,single,multi}.sh` — iterate a regime and
  call the corresponding `*_prompt.sh` worker per sample. `empty` drivers read
  rows from a `--csv`; `single`/`multi` drivers `copytree` each `<pid>` dataset
  dir into `workspace_<agent>/…/<pid>` (leaving the dataset untouched) and send a
  fixed "complete the code at `<FILL_HERE>`" prompt.

Batch drivers embed a Python heredoc (`python3 - <<'PY'`) for the iteration/
manifest logic; the surrounding bash only parses args and forwards flags. Each
run writes `prompt.txt`, `stdout.txt`, `stderr.txt`, `row.json`/manifest, and
(OpenHands) `events.json` under `batch_runs/<batch>/<pid>/`.

When editing a driver's loop, dataset copy, or manifest logic, edit the Python
heredoc, not the bash wrapper.

### Agent-specific mechanics

- **OpenHands** (`run_oh_prompt.sh`): starts a local uvicorn backend
  (`openhands.app_server.app:app`, default port 3300), drives it over its REST
  API, and runs the agent in a **Docker** sandbox with the host workspace
  bind-mounted at `/workspace/project` (`SANDBOX_VOLUMES`). Requires Docker.
  The backend launcher is resolved in order: `poetry` → `.venv/bin/python` →
  system `python3`, each checked for `uvicorn` + `openhands.agent_server` +
  `openhands.app_server` importability. Startup always clears the target port
  first. Detects agent file changes by sha256-diffing the workspace before/after.
- **SWE-agent** (`run_swe_prompt.sh`): requires `--env.repo.path` to be a git
  repo; the worker auto-`git init`s the workspace if needed. Existing repos must
  be clean or SWE-agent refuses to copy them.
- **Codex** (`run_codex_prompt.sh`): shells out to `codex exec --cd <workspace>
  --sandbox <mode> --skip-git-repo-check`. Default sandbox `workspace-write`;
  approval via `--approval` → `--ask-for-approval`.

## Common commands

Setup:

```bash
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
git submodule update --init          # populate SWE-agent/ and codex/
export OPENAI_API_KEY="..."
```

Smoke-test any regime by adding `--limit 1` before running a full split. Model
and key flags differ per agent (see README for the full option tables):

```bash
# OpenHands (needs Docker); empty takes --csv, single/multi don't
./run_oh_empty.sh  --csv jaws_bench_dataset/empty/t2c_l1.csv --limit 1 \
  --model openai/gpt-5-mini --api-key-env OPENAI_API_KEY
./run_oh_single.sh --limit 1 --model openai/gpt-5-mini --api-key-env OPENAI_API_KEY

# SWE-agent
./run_swe_empty.sh  --csv jaws_bench_dataset/empty/t2c_l1.csv --limit 1 --model gpt-5-mini
./run_swe_single.sh --limit 1 --model gpt-5-mini

# Codex (empty uses --csv-file)
./run_codex_empty.sh  --csv-file jaws_bench_dataset/empty/t2c_l1.csv --model gpt-5-mini --approval never
./run_codex_single.sh --model gpt-5-mini --approval never
```

Useful flags on batch drivers: `--limit N`, `--start-pid PID` (resume),
`--server-port` (OpenHands), `--dry-run` (SWE-agent worker).

Note the per-agent naming inconsistency for the CSV flag: OpenHands/SWE use
`--csv`, Codex uses `--csv-file`.
