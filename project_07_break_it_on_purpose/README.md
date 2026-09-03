# Project 07 — Break It On Purpose

A project demonstrating observability and cost measurement in a loop: first measuring what one run actually costs, then deliberately breaking the loop, and proving the failure can be diagnosed from the spine alone — without re-running anything.

## What This Project Does

This project reuses the "morning brief" loop from Project 03 (scanning for TODO comments and updating `progress.md`). It measures the cost of one run, projects a monthly cost at a given cadence, then deliberately points the loop at a folder that doesn't exist — and confirms the failure is fully diagnosable just by reading `progress.md`.

## Files

* `app.py` — copied from Project 03; contains 2 intentional TODO comments
* `progress.md` — the spine: contains the original discovery, a re-confirmation run, and a deliberate failure entry
* `README.md` — this file

## How to Use

### Step 1: Measure One Beat

Start Claude Code in this folder and run the same prompt used in Project 03:

```text
Read progress.md if it exists in this folder. Then scan this repo for open TODO comments (search .py files). Write a short summary of what you found. Then update progress.md: add a "Done" entry with today's date listing the TODOs you found.
```

After it finishes, check the cost of that one run:

```text
/cost
```

### Step 2: Project the Monthly Cost

Multiply the one-run cost by how often the loop would actually run (its cadence).

For example:

```text
Daily cadence:  $0.59/run × 30 days     = ~$17.70/month

Hourly cadence: $0.59/run × 24 × 30     = ~$424.80/month
```

Cadence changes cost dramatically — this is Concept 13's math applied to a real loop, not a hypothetical one.

### Step 3: Sabotage the Loop on Purpose

Give Claude a prompt that can never succeed — a path that doesn't exist — and explicitly require it to leave a clear failure note rather than fail silently:

```text
Read progress.md if it exists in this folder. Then scan this repo for open TODO comments in nonexistent_folder/*.py files. If the folder or files don't exist, log a clear "needs a human" note in progress.md explaining exactly what failed and why, with today's date. Do NOT silently skip this — the note must be explicit enough that someone reading only progress.md later understands the failure without re-running anything.
```

### Step 4: Diagnose Using Only the Spine

```bash
cat progress.md
```

Without asking Claude anything else, and without re-running the loop, answer from this file alone:

* What failed?
* When did it fail?
* Why did it fail?
* Did the loop leave an explicit note, or fail silently?

If the answer to the last question is "it failed silently," the fix is to add a log line before doing anything else — a loop that fails without a trace is worse than one that fails loudly.

## Result

* **Cost per beat:** $0.59 (this run included extra conversational context; a lean, focused production prompt would likely cost less)
* **Projected monthly cost (daily cadence):** ~$17.70/month
* **Sabotage:** pointed the scan at `nonexistent_folder`, which does not exist
* **Diagnosis:** `progress.md` recorded the exact date, the exact tool error, and a clear statement that the path — not the code — was invalid. No re-run was needed to understand what happened.

## How This Differs From Project 03

Project 03 proved the spine remembers between runs. Project 07 proves the spine is also enough to debug a failure after the fact, and adds the missing piece Project 03 never covered: knowing what a loop actually costs to run, and how that cost scales with how often it fires.

## Requirements

* Git Bash (or another bash-compatible shell) on Windows
* Claude Code CLI installed and logged in

## Project Structure

This is a throwaway learning project, built on a copy of Project 03's files so the original Project 03 spine stays untouched.

## Key Lesson

A loop is only trustworthy in production if two things are true: you know what it costs at its real cadence, and when it breaks, it tells you why without needing to be re-run.

A loop that fails silently gives you nothing to diagnose — the fix, always, is a log line before anything else.
