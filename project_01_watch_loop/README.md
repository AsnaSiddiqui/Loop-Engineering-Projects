# Project 01 — In-Session Watch Loop

A simple project demonstrating how to monitor a long-running task using Claude Code's built-in `/loop` command (an in-session heartbeat).

## What This Project Does

This project starts a long-running background task (a shell script that sleeps for 3 minutes, then creates a `result.txt` file). Claude Code's `/loop` command checks every 1 minute whether the task has finished, and reports the moment it has — without anyone watching the terminal.

## Files

* `long_task.sh` — simulates a long-running task (sleeps 180 seconds, then writes `done` to `result.txt`)
* `README.md` — this file

## How to Use

### Step 1: Start the Long-Running Task

In your terminal (Git Bash), make the script executable and run it in the background:

```bash
chmod +x long_task.sh
./long_task.sh &
```

You'll see:

```text
Task started...
```

The script keeps running in the background for 3 minutes.

### Step 2: Start Claude Code in This Folder

```bash
claude
```

Trust the folder when asked.

### Step 3: Start the Watch Loop

Inside Claude Code, run:

```text
/loop 1m check if result.txt exists in this folder; if it does, tell me the task is finished and then cancel this loop
```

### Step 4: Wait for Completion

Claude checks every minute. After approximately 3 minutes, once `result.txt` exists, Claude reports:

```text
Result.txt now exists! The task is finished.
```

### Step 5: Confirm the Loop Stopped

The loop may not always auto-cancel cleanly. Verify with:

```text
show my running loops
```

If anything is still listed, cancel it manually:

```text
cancel the watch loop
```

## How the Loop Works

Claude Code's `/loop` command builds an in-session heartbeat:

1. **Interval-based check** — `/loop 1m` schedules a recurring check every 1 minute using a cron-style job, for as long as the session is open.
2. **Condition check** — Each minute, Claude checks whether `result.txt` exists in the folder.
3. **Report once** — As soon as the file is found, Claude reports that the task is finished instead of repeating the message every minute.
4. **Self-cancel (or manual cancel)** — The loop is designed to cancel itself once done. If it doesn't, `cancel the watch loop` stops it cleanly.
5. **Session-bound** — This loop only runs while the Claude Code session is open. Closing the terminal stops it — that's the defining trait of an in-session loop (Concept 4).

## Stopping the Loop

You can stop the loop early at any time by telling Claude:

```text
cancel the watch loop
```

Or by closing the Claude Code session entirely.

## Requirements

* Git Bash (or another bash-compatible shell) on Windows
* Claude Code CLI installed and logged in
* No external packages required

## Project Structure

This is a throwaway learning project. No persistent state beyond `result.txt`, which is created automatically once the simulated task completes.

## Key Lesson

An in-session loop (`/loop`) only runs while the session stays open, and it doesn't always guarantee a clean self-cancel. Verifying with `show my running loops` and cancelling manually is good practice — never assume a loop stopped itself.
