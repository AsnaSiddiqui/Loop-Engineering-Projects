# Project 08 — Your Own Daily Loop

A project demonstrating how to design and run a daily loop using Claude Code — the final heartbeat type that completes the set of four: in-session, conditional, scheduled, and now daily.

## What This Project Does

This project shows you how to set up a daily loop that runs on a schedule, checks for work to do, processes it, and records its findings — all without a human needing to type a prompt each time. It's the fourth and final heartbeat type, completing the set:

1. **In-session** (`/loop`) — runs while the session is open (Project 01)
2. **Conditional** (`/goal`) — runs until a real command says the work is done (Project 02)
3. **Scheduled** (`/schedule`) — runs at fixed times regardless of session state (Project 03)
4. **Daily** — runs once per day, typically at a set time, using the loop engine with a scheduled trigger

This project demonstrates how to configure a daily loop that:
- Scans for tasks or TODO items each morning
- Processes what it finds
- Records results in `progress.md` (the spine)
- Leaves explicit notes if anything fails or needs human attention
- Can be projected for monthly cost at a given cadence

## Files

- `app.py` — a small file with 2 intentional TODO comments, simulating recurring work
- `progress.md` — the spine: created by Run 1, read and checked by Run 2, and each subsequent run
- `README.md` — this file
- `.claude/skills/daily-freshness-check/SKILL.md` — the daily freshness check skill
- `.claude/agents/reviewer.md` — the reviewer subagent (read-only)

## How to Use

### Step 1: Start Claude Code in This Folder

```bash
claude
```

Trust the folder when asked.

### Step 2: Set Up the Daily Loop

Inside Claude Code, configure the daily loop. The loop will:

1. **Read `progress.md`** if it exists, to recognize what was already found
2. **Scan for TODO comments** in `app.py` (or whatever file contains the work)
3. **Update `progress.md`** with a dated entry of what was found
4. **Leave a clear note** if anything doesn't work (e.g., a path that doesn't exist)

Run the loop once to seed `progress.md`:

```text
Read progress.md if it exists in this folder. Then scan this repo for open TODO comments in app.py. Write a short summary of what you found. Then update progress.md: add a "Done" entry with today's date listing the TODOs you found, in this format:

### Done

- <date>: found N TODO comments: <list them briefly>

### Open / needs a human

- <anything unresolved>
```

### Step 3: Run the Loop a Second Time

Give the **exact same prompt** again. This time Claude reads `progress.md` first, sees the TODOs are already recorded, and does **not** add a duplicate entry — it recognizes the work as already done.

### Step 4: Confirm the Spine Worked

```bash
cat progress.md
```

There should be only **one** "Done" entry, not two. If Run 2 had added a second identical entry, the spine would not be working.

### Step 5: (Optional) Project Monthly Cost

Run `/cost` after one beat, then multiply by your cadence:

```
Daily cadence:  $<cost>/run × 30 days = ~$<projected>/month
Hourly cadence: $<cost>/run × 24 × 30     = ~$<projected>/month
```

### Step 6: Sabotage the Loop on Purpose (Optional)

Give Claude a prompt that can never succeed — a path that doesn't exist — and explicitly require it to leave a clear failure note:

```text
Read progress.md if it exists in this folder. Then scan this repo for open TODO comments in nonexistent_folder/*.py files. If the folder or files don't exist, log a clear "needs a human" note in progress.md explaining exactly what failed and why, with today's date. Do NOT silently skip this — the note must be explicit enough that someone reading only progress.md later understands the failure without re-running anything.
```

### Step 7: Diagnose Using Only the Spine

```bash
cat progress.md
```

Without asking Claude anything else, and without re-running the loop, answer from this file alone:
- What failed?
- When did it fail?
- Why did it fail?
- Did the loop leave an explicit note, or fail silently?

## How the Loop Works

This is a **daily loop** (Concept 14), the fourth heartbeat type:

1. **Scheduled trigger** — the loop fires at a set time each day (e.g., 9am), independent of whether a Claude session is open
2. **Read the spine first** — every run reads `progress.md` before doing any work, so it knows what has already been found
3. **Do the work** — scan for TODO comments, process tasks, or whatever the loop is designed to do
4. **Update the spine last** — write a dated entry recording what was found, so the next run can build on it instead of repeating it
5. **The model itself has no memory between runs** — Claude Code forgets everything once a session ends. The only reason later runs "remember" is that the state lived outside the model, in `progress.md` on disk
6. **In production, this becomes a real schedule** — with `/schedule every day at 9am, ...`, this same prompt would run daily unattended, and `progress.md` would keep growing as the real memory of the loop over time
7. **Cost awareness** — each run costs money; knowing the per-run cost at your cadence lets you project monthly spend (Concept 13's math)

## Requirements

- Git Bash (or another bash-compatible shell) on Windows
- Claude Code CLI installed and logged in
- Python 3.x (for running `app.py` if needed)
- No external packages required for the basic loop

## Project Structure

This is a throwaway learning project, built on concepts from Projects 01–07. The key reusable parts are:

- `progress.md` — the spine that carries state between runs
- The daily loop prompt pattern: read spine → do work → update spine
- The cost-projection math: per-run cost × cadence = monthly cost

## Key Lesson

A daily loop needs three things to be trustworthy in production: a **scheduled trigger** that fires it without a human typing a prompt, a **progress file** (`progress.md`) that every run reads first and updates last so state persists across sessions, and **cost awareness** so you know what the loop costs at its real cadence. Without all three, it's just repetition without reliable state, timing, or economics — and you won't know it's broken until much later.

**The spine is the single most important part:** `progress.md`, read at the start and updated at the end of every run, is what turns a daily repetition into a real loop with memory, debuggability, and predictable cost. Without it, every run is identical — the same first step, repeating forever, no matter how smart the model is.

---

**This completes the set of four heartbeat types** in the freshness-run-2 series:
- Project 01: In-session loop (`/loop`)
- Project 02: Conditional loop (`/goal`)
- Project 03: Scheduled loop with memory (`/schedule`)
- Project 04: Fix loop with a real checker (maker-checker)
- Project 05: Engine, not a loop (three bugs, three worktrees)
- Project 06: Event-driven loop (GitHub PR trigger)
- Project 07: Observability and cost measurement
- **Project 08: Daily loop** (scheduled daily trigger + progress spine)