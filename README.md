# JAWS-Bench

JAWS-Bench (Jailbreaks Across WorkSpaces) is a benchmark for evaluating the
safety of code agents under increasingly realistic workspace conditions. It was
introduced in the paper:

**Breaking the Code: Security Assessment of AI Code Agents Through Systematic Jailbreaking Attacks** ([Paper Link](https://arxiv.org/abs/2510.01359))


## Responsible Use

This is a **defensive security research** benchmark. The `jaws_bench_dataset/`
directory contains malicious and harmful code samples (e.g. malware, keyloggers,
ransomware) **by design** — they are the stimuli used to measure whether code
agents refuse malicious coding requests, not code intended for real-world use.

The dataset and harness are released solely to support research on the safety
and robustness of AI code agents. By using this repository you agree to use it
only for lawful, ethical, defensive research and evaluation, and not to deploy,
distribute, or repurpose any sample to cause harm. The samples are provided
"as is" without warranty; the authors accept no liability for misuse.


## What This Repository Contains

```text
.
├── jaws_bench_dataset/
│   ├── empty/          # JAWS-0 prompt-only CSV tasks
│   ├── single_file/    # JAWS-1 single-file completion workspaces
│   └── multi_file/     # JAWS-M multi-file completion workspaces
├── OpenHands/          # OpenHands snapshot used by the experiments
├── SWE-agent/          # SWE-agent snapshot used by the experiments
├── codex/              # Codex CLI/agent snapshot used by the experiments
├── run_oh_*.sh         # OpenHands benchmark runners
├── run_swe_*.sh        # SWE-agent benchmark runners
└── run_codex_*.sh      # Codex benchmark runners
```

The `OpenHands/` directory is vendored in this repository because we made
evaluation-specific changes to OpenHands for JAWS-Bench. These changes were
implemented on top of upstream OpenHands commit
[`0571ff530fa6114360feb10d2d1a0c2570987450`](https://github.com/OpenHands/OpenHands/commit/0571ff530fa6114360feb10d2d1a0c2570987450).

The runner scripts can create these directories automatically during experiments:

- `workspace_oh/`, `workspace_swe/`, and `workspace_codex/` store per-sample
  workspaces copied from the benchmark data and modified by the agents.
- `batch_runs/` stores prompts, stdout, stderr, manifests, traces, and event
  logs.
- `openhands-backend-*.log` is created when the OpenHands backend starts.

## Benchmark Regimes

JAWS-Bench has three regimes:

| Regime | Folder | Attacker model | Task form |
| --- | --- | --- | --- |
| JAWS-0 | `jaws_bench_dataset/empty/` | Naive attacker | Prompt-only generation from an empty workspace |
| JAWS-1 | `jaws_bench_dataset/single_file/` | Capable attacker | Complete an incomplete single-file workspace at `<FILL_HERE>` |
| JAWS-M | `jaws_bench_dataset/multi_file/` | Expert attacker | Complete an incomplete multi-file workspace at `<FILL_HERE>` |

## Dataset Sizes

| Split | Count |
| --- | ---: |
| JAWS-0 Level 1 prompts | 80 |
| JAWS-0 Level 2 prompts | 102 |
| JAWS-1 single-file workspaces | 100 |
| JAWS-M multi-file workspaces | 180 |

The JAWS-0 CSV files contain metadata such as `pid`, `category`, `task`,
`prompt`, `language`, `source`, and `jid`. The JAWS-1 and JAWS-M folders are
organized by sample id, with each id containing the workspace files provided to
the agent.


## Setup

Clone the repository and install the dependencies for the agent you want to run.
Each agent directory is an upstream project snapshot, so refer to that project's
installation instructions for complete setup details.

The provided Python environment can be installed with:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

At minimum, set the model provider credentials in your shell:

```bash
export OPENAI_API_KEY="..."
```

For OpenHands experiments, Docker must be available because OpenHands runs agent
workspaces in containers. For SWE-agent experiments, each workspace is
automatically initialized as a git repository before the run.


## Running OpenHands

OpenHands runs require Docker and a model API key. The wrapper scripts start the
OpenHands backend, create a workspace for each benchmark sample, send the task
prompt to OpenHands, and save logs under `batch_runs/`.

First, set your key:

```bash
export OPENAI_API_KEY="..."
```

Then run a small smoke test before launching a full benchmark split.

Run one JAWS-0 prompt:

```bash
./run_oh_empty.sh \
  --csv jaws_bench_dataset/empty/t2c_l1.csv \
  --limit 1 \
  --model openai/gpt-5-mini \
  --api-key-env OPENAI_API_KEY
```

Run all JAWS-0 Level 1 prompts by removing `--limit 1`:

```bash
./run_oh_empty.sh \
  --csv jaws_bench_dataset/empty/t2c_l1.csv \
  --model openai/gpt-5-mini \
  --api-key-env OPENAI_API_KEY
```

Run one JAWS-1 sample:

```bash
./run_oh_single.sh \
  --limit 1 \
  --model openai/gpt-5-mini \
  --api-key-env OPENAI_API_KEY
```

Run one JAWS-M sample:

```bash
./run_oh_multi.sh \
  --limit 1 \
  --model openai/gpt-5-mini \
  --api-key-env OPENAI_API_KEY
```

The main OpenHands options are:

| Option | Meaning |
| --- | --- |
| `--csv` | JAWS-0 CSV file to process |
| `--dataset-root` | JAWS-1 or JAWS-M sample directory |
| `--workspace-root` | Where copied workspaces are generated |
| `--runs-dir` | Where run logs and manifests are generated |
| `--limit` | Number of samples to run |
| `--start-pid` | Start from a specific sample id |
| `--model` | Model name passed to OpenHands |
| `--api-key-env` | Environment variable containing the model API key |
| `--server-port` | Local OpenHands backend port |

OpenHands outputs are generated under `batch_runs/`, copied workspaces are
generated under `workspace_oh/`, and backend logs are generated as
`openhands-backend-*.log`.

## Running SWE-agent

Run one JAWS-0 prompt:

```bash
./run_swe_empty.sh \
  --csv jaws_bench_dataset/empty/t2c_l1.csv \
  --limit 1 \
  --model gpt-5-mini
```

Run one JAWS-1 sample:

```bash
./run_swe_single.sh \
  --limit 1 \
  --model gpt-5-mini
```

Run one JAWS-M sample:

```bash
./run_swe_multi.sh \
  --limit 1 \
  --model gpt-5-mini
```

SWE-agent outputs are written under `batch_runs/swe_*`, and copied workspaces
are created under `workspace_swe/`.

## Running Codex

Run one JAWS-0 prompt:

```bash
./run_codex_empty.sh \
  --csv-file jaws_bench_dataset/empty/t2c_l1.csv \
  --model gpt-5-mini \
  --approval never
```

Run one JAWS-1 sample:

```bash
./run_codex_single.sh \
  --model gpt-5-mini \
  --approval never
```

Run one JAWS-M sample:

```bash
./run_codex_multi.sh \
  --model gpt-5-mini \
  --approval never
```

Codex copied workspaces are created under `workspace_codex/`.


## Judge Framework 

JAWS-Bench uses a two-stage evaluation pipeline that judges the final workspace:

1. **Robustness Judge:** evaluates attack success and compliance.
2. **Executability Judge:** evaluates syntax correctness, and
   runtime executability.

See the [judge framework](judge_framework/README.md) for requirements, usage,
output formats, and commands for running and combining both judges.


## License

The JAWS-Bench code and dataset authored by Amazon are licensed under
[CC-BY-NC-4.0](LICENSE) (Creative Commons Attribution-NonCommercial 4.0
International).

This repository also incorporates third-party material under their own licenses,
including RMCBench (CC BY 4.0), a vendored MIT-licensed OpenHands snapshot, and
the SWE-agent and Codex submodules. See [THIRD-PARTY-LICENSES](THIRD-PARTY-LICENSES)
for full attributions and terms.


## Citation

```bibtex
@misc{saha2026breakingcodesecurityassessment,
      title={Breaking the Code: Security Assessment of AI Code Agents Through Systematic Jailbreaking Attacks}, 
      author={Shoumik Saha and Jifan Chen and Sam Mayers and Sanjay Krishna Gouda and Zijian Wang and Varun Kumar},
      year={2026},
      eprint={2510.01359},
      archivePrefix={arXiv},
      primaryClass={cs.CR},
      url={https://arxiv.org/abs/2510.01359}, 
}
```
