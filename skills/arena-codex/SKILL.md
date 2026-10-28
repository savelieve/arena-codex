---
name: arena-codex
description: Compare independent solutions through a tournament of strategy cards, adversarial critique, revision, and rubric-based judging. Use when the user requests an arena or competing approaches to a difficult task; an ordinary correction or retry alone does not require a tournament.
---

# Arena for Codex

Run independent competitors on one task, then eliminate candidates through attack, defense,
and judging rounds. The orchestrator coordinates; it does not compete, judge, or invent verdicts.
Requires Python 3.8+ and available Codex subagent tools. The script needs no API keys or Python
packages; model calls still consume usage. This skill explicitly calls for parallel subagent work
when performing a tournament, subject to host permissions. Reading or installing it does not start one.

## Size the run

Read the task and flags from the user's message, without slash-command interpolation. With no
task, use the latest substantive request and, if relevant, the rejected answer as a baseline.

| Option | Meaning |
| --- | --- |
| `--agents N` | Competitors, default 100, preserving the original Arena behavior. |
| `--quick` | 16 competitors. Mutually exclusive with `--agents`. |
| `--seed S` | Reproducible cards and bracket, not deterministic model answers. |
| `--wave W` | Batch size, default 3. Cap to actual available worker slots. |

Resolve this skill's absolute directory from its loaded location. Below, `ARENA` means
`python "<absolute skill directory>/bracket.py"`; it is notation, not an executable alias.
Use the host's working Python executable (`python`, `python3`, or `py -3`).

Run `ARENA plan --agents N --wave W` (substitute `--quick` when requested). Report competitors,
rounds, and projected calls, plus one final judge call if using a baseline. The full run uses
595 calls before retries; quick uses 91. Competitor count is not concurrent worker count.
Respect the user's budget; do not silently shrink the run.

An explicit tournament request authorizes starting within scope. If proposing this as an optional
escalation, obtain agreement to its cost before launching workers. If subagents are unavailable
or forbidden, report the limitation; do not simulate independent judges in the main conversation.

## Prepare identical context

Write a standalone UTF-8 task file under `.arena/` in the task workspace. Include the request,
constraints, acceptance criteria, relevant absolute paths, essential data, and applicable project
rules. Do not bias it toward a solution or invent requirements. With a baseline, save the rejected
answer verbatim in a separate UTF-8 file.

Run `ARENA init --agents N --wave W --task-file "<task file>"`, optionally adding `--seed S`
and `--baseline-file "<baseline file>"`. Choose a unique directory with `--dir "<absolute run>"`.
Pass the same `--dir` to subsequent commands so another run cannot redirect this one through
the shared `.arena/LATEST` pointer.

## Orchestrate

1. Run `ARENA next --dir "<run>"` to determine the phase.
2. Run `ARENA prompts <phase> --dir "<run>"` to generate briefs and list missing jobs.
3. Start one fresh subagent per job, at most one available wave at a time. With the collaboration
   API, use `spawn_agent`, a unique lowercase task name, `fork_turns: "none"`, and message
   `Read <absolute prompt path> and follow it. It is your whole task brief.` Omit model/reasoning
   overrides unless explicitly requested. Use the host's actual schema, not Claude Agent fields.
4. Wait for all jobs in a wave to finish and inspect receipts. Fresh contexts preserve independence;
   do not reuse a competitor as its judge. Workers must not delegate. Release completed workers
   if supported. If capacity cannot be recovered, preserve state and report the limitation.
5. Run `ARENA check <phase> --dir "<run>"` and `ARENA next --dir "<run>"`. Files determine
   completion; a worker's DONE message alone is insufficient.

Sequence: spawn, then attack -> defend -> judge -> collect -> advance for each round. An optional
final phase compares champion and baseline, followed by collect. Only the orchestrator runs
state-changing bookkeeping. Never advance before dependencies complete. `collect` validates and
records judgments. Reserve `record` for user-requested bookkeeping repairs.

The script loads [references/prompts.md](references/prompts.md) to define each role and output
format. Judges use [rubric.md](rubric.md); cards come from `strategies.json`. Do not customize
one competitor's generated task or brief. The task must remain identical across all competitors.

### Failure and resume

Retry missing output once. After two failed attempts, a missing attack may be recorded as
`NO OUTPUT` in its assigned file; disclose degraded coverage. For a missing solution, defense,
or invalid/missing verdict, stop at that phase and report affected jobs instead of inventing
content. A judge may receive one additional fresh attempt (three total). Preserve failed artifacts.

After interruption or compaction, use `status` then `next` with the explicit run directory.
Give brief, regular progress updates, including remaining competitors after each round.
Stop when asked, preserving state for continuation.

## Deliver

When `next` reports DONE, run `winner` and read its reported solution. During the run, normally
read bookkeeping and receipts instead of all candidates; inspect relevant artifacts for failures
or suspected scope violations.

Return the winning solution, attacks survived, strategy card, round and competitor counts, and
record location. Report baseline scores honestly, even if the baseline won. Surface unresolved
fatal flaws or missing reviews; surviving the bracket is not proof of correctness.

Workers confine writes to assigned run outputs or scratch paths. This is an instruction boundary,
not an OS sandbox. They may read task-authorized sources but cannot mutate external services.
Candidate code is returned as a diff or file content. Apply it only when existing user instructions
authorize implementation; otherwise obtain authorization for the concrete result. A tournament
alone does not authorize project edits, messages, merges, deployments, or financial operations.
