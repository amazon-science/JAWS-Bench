# Executability Judge

This is Stage 2 of the JAWS-Bench evaluation framework. It uses an OpenHands
agent to inspect and test final workspaces, then writes three verdicts to each
workspace's `judge_output.json`:

- `parseability`
- `syntax_error_free`
- `runtime_error_free`

Run all commands below from the JAWS-Bench repository root.

## Required customized OpenHands agent

This directory intentionally does **not** include `judge.md`. You must use the
customized OpenHands agent provided with JAWS-Bench. Before running, verify:

```bash
test -f OpenHands/skills/judge.md
```

The runner checks this requirement and stops with an explanatory error when
the skill is absent. A stock OpenHands checkout without this skill is not a
valid executability judge for JAWS-Bench.

OpenHands also requires its normal backend dependencies, Docker, and the API
key for the selected model:

```bash
export OPENAI_API_KEY="..."
```

By default, the relocated runner resolves OpenHands at the repository-level
`OpenHands/` directory and the Python environment at `.venv/`. Override the
agent location with `--repo-dir` if necessary.

## Prepare judge workspaces

The judge writes `judge_output.json` into every evaluated PID directory and
may execute workspace code. Evaluate a separate copy rather than the original
agent-output directory. Existing examples use:

```text
workspace_oh_judge/empty/<pid>/
workspace_oh_judge/single/<pid>/
workspace_oh_judge/multi/<pid>/
```

The same convention can be used for Codex and SWE-agent results. The
`--workspace-base` argument must contain the literal `{pid}` placeholder.

## JAWS-0

```bash
python judge_framework/executability_judge/run_judge_agent.py \
  --execute \
  --workspace-base 'workspace_oh_judge/empty/{pid}' \
  --model openai/gpt-5.1
```

## JAWS-1

```bash
python judge_framework/executability_judge/run_judge_agent.py \
  --execute \
  --workspace-base 'workspace_oh_judge/single/{pid}' \
  --model openai/gpt-5.1
```

## JAWS-M

```bash
python judge_framework/executability_judge/run_judge_agent.py \
  --execute \
  --workspace-base 'workspace_oh_judge/multi/{pid}' \
  --model openai/gpt-5.1
```

The shell wrapper forwards the same arguments:

```bash
judge_framework/executability_judge/run_judge_agent.sh \
  --execute \
  --workspace-base 'workspace_oh_judge/single/{pid}'
```

## Smoke tests and selection

Use `--dry-run` to inspect the PID, workspace, prompt, model, and server
without starting OpenHands. Use `--filter` to select PIDs:

```bash
python judge_framework/executability_judge/run_judge_agent.py \
  --execute \
  --dry-run \
  --filter 'pid == 183' \
  --workspace-base 'workspace_oh_judge/single/{pid}'
```

Raw OpenHands events can be retained with `--dump-events-dir PATH`. Backend
startup, wait, polling, endpoint, API-key, and server-port options are listed
by `--help`.

## Output

Each completed PID should contain:

```text
<judge-workspace>/<pid>/judge_output.json
```

The prompt explicitly requires OpenHands to write the container path
`/workspace/project/judge_output.json`, which corresponds to that host path.
After every completed conversation, the runner validates the PID and the three
required verdict/reasoning sections. If the file was mistakenly written to a
probable alternate path such as `/workspace/judge_output.json`, the runner
recovers the JSON from the recorded OpenHands file-write event, normalizes a
legacy `reason` field to `reasoning`, and persists it in the correct PID
workspace. A completed conversation is reported as failed when neither a valid
persisted file nor a valid recoverable event payload exists.

Use `judge_framework/combine_judge_outputs.py` to merge these files with the
two robustness-judge result files.
