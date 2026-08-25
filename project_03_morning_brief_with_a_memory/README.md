# Project 03 — Scheduled Loop with Memory: The Morning Brief

A project demonstrating a scheduled loop that remembers what it found last time, using a progress file (the "spine") instead of relying on the model's own memory.

## What This Project Does

This project scans a repo for open `TODO` comments and writes a summary into `progress.md`. The key test: run it twice. The second run must read `progress.md` first and recognize what was already found, instead of reporting the same TODOs as new discoveries again.

## Files

* `app.py` — a small file with 2 intentional `TODO` comments, simulating a real repo
* `progress.md` — the spine: created by Run 1, read and checked by Run 2
* `README.md` — this file

## How to Use

### Step 1: Start Claude Code in This Folder

```bash
claude
```

Trust the folder when asked.

### Step 2: Run 1 — First Pass

Give Claude this prompt:

```text
Read progress.md if it exists in this folder. Then scan this repo for open TODO comments (search .py files). Write a short summary of what you found. Then update progress.md: add a "Done" entry with today's date listing the TODOs you found, in this format:

### Done

- <date>: found N TODO comments: <list them briefly>

### Open / needs a human

- <anything unresolved>

If progress.md doesn't exist yet, create it.
```

Since `progress.md` doesn't exist yet, Claude creates it and records the 2 TODOs found in `app.py`, with today's date.

### Step 3: Run 2 — Second Pass (The Real Test)

Give Claude the **exact same prompt** again, in the same or a new session.

This time Claude reads `progress.md` first, sees the 2 TODOs are already recorded, and does **not** add a duplicate entry — it recognizes the work as already done.

### Step 4: Confirm the Spine Worked

```bash
cat progress.md
```

There should be only **one** "Done" entry, not two. If Run 2 had added a second identical entry, the spine would not be working — that would mean the loop has no memory and starts from zero every run.

## How the Loop Works

This is a scheduled loop (Concept 6) using a progress file as its spine (Concept 12):

1. **Read the spine first** — every run reads `progress.md` before doing any work, so it knows what has already been found.
2. **Do the work** — scan `.py` files for `TODO` comments.
3. **Update the spine last** — write a dated entry recording what was found, so the next run can build on it instead of repeating it.
4. **The model itself has no memory between runs** — Claude Code forgets everything once a session ends. The only reason Run 2 "remembered" the TODOs is that the state lived outside the model, in a plain markdown file on disk.
5. **In production, this becomes a real schedule** — with `/schedule every day at 9am, ...`, this same prompt would run daily unattended, and `progress.md` would keep growing as the real memory of the loop over time.

## Requirements

* Git Bash (or another bash-compatible shell) on Windows
* Claude Code CLI installed and logged in
* No external packages required

## Project Structure

This is a throwaway learning project. State lives entirely in `progress.md`, which is the point of the exercise — the repo remembers what the model cannot.

## Key Lesson

A loop is only a loop if something outside the model carries state between runs. Without a progress file, every run is identical — the same first step, repeating forever, no matter how smart the model is. `progress.md`, read at the start and updated at the end of every run, is what turns repetition into progress.
