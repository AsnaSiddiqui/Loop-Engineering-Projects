# Project 02 — Conditional Loop: Make the Tests Pass, Then Stop

A project demonstrating a conditional loop that runs until a real command — not the agent itself — decides the work is done.

## What This Project Does

This project starts with a Python file containing 3 intentional bugs and a test file with 3 failing tests. Claude Code's `/goal` command keeps fixing the code until `pytest` actually reports all tests passing. A separate checker (not the agent) verifies success using the test runner's output as proof.

## Files

* `calculator.py` — starts with 3 intentional bugs
* `test_calculator.py` — 3 tests that fail against the buggy code
* `README.md` — this file

## How to Use

### Step 1: Confirm the Tests Fail (Starting Point)

```bash
pytest
```

Expected output: 3 failed tests, since `calculator.py` has bugs.

### Step 2: Start Claude Code in This Folder

```bash
claude
```

Trust the folder when asked.

### Step 3: Start the Conditional Loop

Inside Claude Code, run:

```text
/goal Make all 3 tests in test_calculator.py pass by fixing the bugs in calculator.py. Run pytest and show me the output as proof. Stop after 6 attempts if not solved, and tell me which tests are still failing.
```

### Step 4: Let Claude Work

Claude reads the bugs, fixes them, and re-runs `pytest` to check its own work. It keeps trying (up to 6 attempts) until the tests actually pass.

### Step 5: Confirm the Result

When successful, you'll see:

```text
3 passed in 0.65s
✔ Goal achieved
```

## How the Loop Works

Claude Code's `/goal` command builds a conditional (run-until-done) loop:

1. **Draft** — Claude reads the bugs and edits `calculator.py`.
2. **Verify with a command, not opinion** — Claude runs `pytest` and must show the actual output as proof, rather than just claiming the work is done.
3. **Checker decides, not the agent** — a separate process reads the transcript and confirms the stopping condition (`3 passed`) was really met before ending the loop. This is the maker-checker pattern (Concept 11).
4. **Capped retries** — a limit of 6 attempts was set upfront, so the loop can never run forever if the bugs turn out to be harder to fix.
5. **Stops on real success** — the loop ended after 1 attempt because the tests genuinely passed, not because it hit the attempt cap.

## Requirements

* Git Bash (or another bash-compatible shell) on Windows
* Python 3.x with `pytest` installed (`pip install pytest`)
* Claude Code CLI installed and logged in

## Project Structure

This is a throwaway learning project. No persistent state beyond the fixed `calculator.py` file.

## Key Lesson

The stopping condition must be provable by a real command (`pytest`), not by the agent's own claim that it's "done." This is what separates a conditional loop with a real checker from an agent just saying "finished" and hoping it's true.
