# Project 08 — Your Own Daily Loop

A capstone project integrating all six parts of loop engineering into one real, recurring chore: a docs-freshness check across every sibling docs project in this repo — read-only, isolated, and reviewed before anything is merged.

## What This Project Does

The loop checks every sibling `project_0X_*` folder for a fresh `README.md` (present, has a "Key Lesson" section, not suspiciously short), writes the findings into `freshness_report.md`, and records what it found in `progress.md`.

It only ever reads other project folders — it never edits anything outside its own folder. Work is drafted in an isolated worktree, graded by a separate reviewer subagent, and only merged on a PASS verdict.

## The Six Parts, All Present

| Part              | How it appears here                                                                                 |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| **Heartbeat**     | Designed to run on a schedule (daily); validated here with two manual runs standing in for two days |
| **Skill**         | `.claude/skills/daily-freshness-check/SKILL.md` carries all the steps and the hard rule about scope |
| **Spine**         | `progress.md` — read first, updated last, every run                                                 |
| **Worktree**      | Each run drafted in its own isolated worktree (`freshness-run-1`, `freshness-run-2`)                |
| **Maker-checker** | An implementer drafts the report; `.claude/agents/reviewer.md` independently grades PASS/FAIL       |
| **Connector**     | A PR is opened only on PASS, and merged into `main`                                                 |

## Files

* `.claude/skills/daily-freshness-check/SKILL.md` — the implementer's steps
* `.claude/agents/reviewer.md` — the read-only reviewer subagent
* `progress.md` — the spine, with dated entries from both runs
* `freshness_report.md` — the latest freshness findings
* `README.md` — this file

## How This Was Built

### Step 1: Measure a Safe Scope

The skill's hard rule: only `Read` other project folders, only `Edit`/`Write` inside `project_08_your_own_daily_loop/`.

The reviewer's first check is always whether that boundary held.

### Step 2: Run 1 — Isolated Worktree

```bash
git worktree add ../freshness-run-1 -b claude/freshness-run-1
cd ../freshness-run-1/project_08_your_own_daily_loop
claude
```

Use the daily-freshness-check skill:

```text
Use the daily-freshness-check skill.
```

Result: 7 of 8 sibling projects had a fresh README; `project_08` itself was missing one (an intentionally honest finding — the loop caught its own gap).

The reviewer subagent graded this **PASS** after confirming scope, accuracy, and a dated `progress.md` entry. The PR was merged into `main`.

### Step 3: Run 2 — Proving the Spine and Closing the Gap

```bash
git worktree add ../freshness-run-2 -b claude/freshness-run-2
cd ../freshness-run-2/project_08_your_own_daily_loop
claude
```

Use the daily-freshness-check skill:

```text
Use the daily-freshness-check skill.
```

This run read `progress.md` from Run 1, saw the missing-README finding was already known, created the missing `README.md` for `project_08` itself, and updated the report to 8/8 fresh.

The reviewer subagent confirmed **PASS**, and also confirmed a report inconsistency spotted mid-run had already been resolved before the final check. The PR was merged.

### Step 4: Clean Up

```bash
git worktree remove ../freshness-run-1 --force
git worktree remove ../freshness-run-2 --force
git branch -D claude/freshness-run-1 claude/freshness-run-2
git push origin --delete claude/freshness-run-1
git push origin --delete claude/freshness-run-2
```

## Result

* **Run 1:** 7/8 projects fresh; `project_08` flagged as missing its own README — reviewer PASS.
* **Run 2:** Spine correctly built on Run 1 instead of rediscovering it; `project_08`'s README was created; 8/8 projects fresh — reviewer PASS.

## Honest Notes on Scope (This Is a Shortened Capstone)

The book specifies running this unattended for a full week before calling it trustworthy.

That wasn't practical here, so this capstone was validated with **two manual runs** standing in for two days, rather than seven days of unattended scheduled execution.

The full six-part shape is real and working; the "ran for a week and I still read every output" trust-building step is the part that was compressed.

Two other real issues came up while building this, both worth recording honestly rather than hiding:

1. **A git merge did not carry file content on the first attempt** — `gh pr merge` reported success, but the committed `progress.md` on `main` stayed at its baseline empty state. This was traced to running `git add`/`git commit` from the wrong working directory (the repo root instead of the worktree) before pushing, so the first "Run 1" commit was empty of real content. It was fixed by committing directly from inside the worktree folder.

2. **The reviewer subagent intermittently returned garbled or failed responses** when run over an OpenRouter-backed model, requiring a retry with an explicit "show me the raw verdict" prompt before a clean PASS was obtained. A production version of this loop should assume occasional reviewer-call failures and retry or escalate rather than silently accepting an unclear response.

## Requirements

* Git Bash (or another bash-compatible shell) on Windows
* Claude Code CLI installed and logged in
* GitHub CLI (`gh`), authenticated

## Key Lesson

A daily loop needs three things to be trustworthy in production:

1. A scheduled trigger that fires it without a human typing a prompt.
2. A progress file that every run reads first and updates last so state survives across sessions.
3. Cost awareness so you know what the loop costs at its real cadence.

Getting the six-part shape right — heartbeat, skill, spine, worktree, maker-checker, connector — is necessary but not sufficient.

Trust is built by watching it run for real, repeatedly, and by fixing the mechanical failures (a wrong working directory, a flaky reviewer call) the first few times they happen, before letting it run unattended.