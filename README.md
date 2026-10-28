# Arena for Codex

A separate Codex adaptation of [Jake Schincariol's Arena skill](https://github.com/Jakeschincariol/arena-skill), retaining the MIT license and original attribution.

Independent competitors receive identical tasks and different strategy cards. Candidates attack, defend, revise, and face rubric-based judges until one remains. The Python CLI persists the bracket and generates briefs; Codex performs model calls.

## Use

Copy `skills/arena-codex` into your Codex skills directory (normally `~/.codex/skills/arena-codex`). Do not overwrite an existing customized copy. The skill is available on the next turn after installation.

```text
Use $arena-codex --quick to compare approaches to this problem: ...
Use $arena-codex --agents 8 --seed 7 to improve this proposal: ...
```

Python 3.8+ and Codex subagent tools are required. Runtime uses Python's standard library only. Default: 100 competitors, 595 model calls; `--quick`: 16 competitors, 91 calls. A baseline adds one call; retries may add more. Model usage still consumes your budget.

## Local checks

From this folder:

```powershell
python -m unittest discover -s tests -v
python skills/arena-codex/bracket.py plan --quick --wave 3
```

Tests simulate agents to exercise bookkeeping and prompt generation. They do not establish real model answer quality or successful host orchestration.

## Adaptation

- Separate identity and Codex UI metadata: `arena-codex`.
- Codex subagent instructions replace Claude tool calls and environment variables.
- Wave size defaults to 3; the orchestrator caps it to available capacity.
- Prompts move to `references/prompts.md`; dealing, scoring, and bracket behavior are retained.
- Explicit run paths avoid relying on the shared latest-run pointer.
- Failed solution/judge jobs stop the workflow instead of fabricating results.

Upstream snapshot: `df07b8e518e10cdecd8cd7712d9958b6f396250e`, retrieved 2026-10-28.
The strategy library, rubric, bracket engine, role templates, and original tests derive from that snapshot. Modified files are maintained independently. The MIT copyright notice is included at the repository root and inside the installable skill.

This is an independently maintained adaptation, with a fresh Git history. Installation does not run a tournament.
