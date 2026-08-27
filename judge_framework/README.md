# JAWS-Bench Judge Framework

This directory brings the two JAWS-Bench evaluation stages under one layout
without changing or removing their original implementations.

```text
judge_framework/
├── README.md
├── combine_judge_outputs.py
├── robustness_judge/
│   ├── README.md
│   ├── judge_agent_model.py
│   └── judge_util.py
└── executability_judge/
    ├── README.md
    ├── run_judge_agent.py
    └── run_judge_agent.sh
```

Run the documented commands from the JAWS-Bench repository root so dataset,
workspace, result, and OpenHands paths resolve consistently.

## Stage 1: robustness judge

The robustness judge sends the original task prompt and serialized final
workspace to a judge model. Two independent passes produce:

- `successful_attack`: `GOOD`, `BAD`, or `UNCLEAR`
- `refusal`: `YES` or `NO`

JAWS-0 reads per-PID prompts from its CSV. JAWS-1 and JAWS-M discover numeric
PID workspace directories and apply one shared completion prompt. See
[`robustness_judge/README.md`](robustness_judge/README.md).

## Stage 2: executability judge

The executability judge runs the customized OpenHands `/judge-workspace` skill
against a copy of each final workspace. It writes `judge_output.json` inside
each PID directory with verdicts for:

- `parseability`
- `syntax_error_free`
- `runtime_error_free`

The framework intentionally does not include `judge.md`. You must use the
customized OpenHands agent supplied with JAWS-Bench, and it must already
contain `OpenHands/skills/judge.md`. See
[`executability_judge/README.md`](executability_judge/README.md).

The runner explicitly targets `/workspace/project/judge_output.json`, validates
the persisted JSON after every completed conversation, and can recover a valid
result from recorded OpenHands file-write events when the agent mistakenly
writes to a probable alternate container path.

## Combining both stages

`combine_judge_outputs.py` merges the two Stage 1 JSON lists with the Stage 2
per-PID files. For example:

```bash
python judge_framework/combine_judge_outputs.py \
  workspace_oh_judge/single \
  --attack_evaluation_json results/oh_jaws1_attack.json \
  --refusal_evaluation_json results/oh_jaws1_refusal.json \
  --output results/oh_jaws1_combined.json
```

For JAWS-0, category metadata can also be loaded from the corresponding CSV:

```bash
python judge_framework/combine_judge_outputs.py \
  workspace_oh_judge/empty \
  --attack_evaluation_json results/oh_jaws0_l1_attack.json \
  --refusal_evaluation_json results/oh_jaws0_l1_refusal.json \
  --malicious_category_csv jaws_bench_dataset/empty/t2c_l1.csv \
  --output results/oh_jaws0_l1_combined.json
```

The combiner takes the union of PIDs found across both stages. A PID may
therefore appear with only the fields available from completed evaluations.

## Existing outputs

The existing top-level `results/` directory remains unchanged. At the time
this framework was created, it contained partial, valid robustness results for
JAWS-0, JAWS-1, and JAWS-M. New commands may continue writing there.
