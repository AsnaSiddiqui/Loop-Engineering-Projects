# Project 04 — A Fix Loop with a Real Checker

A project demonstrating a maker-checker loop: an implementer drafts a fix in an isolated git worktree, and a completely separate reviewer subagent independently grades it PASS or FAIL — before anything is treated as done.

## What This Project Does

A bug in `math_utils.py` breaks a test. An implementer fixes it inside an isolated worktree, and a reviewer subagent (a separate, read-only agent) verifies the fix by actually running the tests itself. The same reviewer is then tested against a deliberately wrong fix, to prove it can catch a bad fix and not just rubber-stamp everything.

## Files

* `math_utils.py` — contains a bug in `average()` (`+ 1` added incorrectly)
* `test_math_utils.py` — a test that fails against the buggy code
* `.claude/skills/fix-loop/SKILL.md` — the implementer's step-by-step skill
* `.claude/agents/reviewer.md` — the reviewer subagent (read-only, grades PASS/FAIL, cannot edit files)
* `README.md` — this file

## How to Use

### Step 1: Confirm the Bug and Failing Test

```bash
pytest
```

Expected: 1 test fails, because `average()` has an extra `+ 1`.

### Step 2: Start Claude Code in This Folder

```bash
claude
```

Trust the folder when asked.

### Step 3: Run the Fix Loop for a Genuinely Good Fix

Inside Claude Code, run:

```text
Do not modify anything in this current folder. Create a new isolated worktree by running: git worktree add ../fix-average-worktree -b claude/fix-average

Then, inside that worktree only, use the fix-loop skill to fix the bug in math_utils.py. Ask the reviewer subagent to grade the diff. Show me its full verdict and reasons.
```

Expected result: reviewer runs the tests itself and replies `PASS`.

### Step 4: Test the Reviewer Against a Deliberately Bad Fix

Create a second worktree manually (safer than trusting the agent to pick the right path):

```bash
git worktree add ../bad-average-worktree -b claude/bad-fix-average
cd ../bad-average-worktree
```

Plant a subtly wrong fix:

```bash
cat > math_utils.py << 'EOF2'
def average(numbers):
    """Return the average of a list of numbers."""
    total = 0
    for n in numbers:
        total += n
    return total / (len(numbers) - 1)   # deliberately wrong fix
EOF2
```

Start Claude Code **inside this worktree folder** (important — the reviewer must be run from the folder containing the bad fix):

```bash
claude
```

Then ask:

```text
Show me the exact contents of math_utils.py in this current folder. Then invoke the reviewer subagent to grade this file against test_math_utils.py. I need the reviewer's actual PASS or FAIL verdict with reasons.
```

Expected result: reviewer replies `FAIL`, with specific reasons (which assertions fail, why, and what the fix should have been).

### Step 5: Clean Up

Once both verdicts are confirmed, remove the temporary worktrees and branches so the repo stays clean:

```bash
cd ../project_04_fix_loop_with_real_checker
git worktree remove ../fix-average-worktree --force
git worktree remove ../bad-average-worktree --force
git branch -D claude/fix-average
git branch -D claude/bad-fix-average
```

## How the Loop Works

This is a maker-checker loop (Concept 11) built on top of a skill (Concept 9) and isolated worktrees (Concept 8):

1. **Skill carries the steps** — `fix-loop/SKILL.md` tells the implementer exactly how to draft a fix, so the prompt stays short.
2. **Isolation** — every fix is drafted in its own git worktree, on its own branch, so parallel or experimental work never collides with `main`.
3. **Maker drafts, checker grades** — the implementer (maker) writes the fix. A separate reviewer subagent (checker), with read-only tools, re-runs the tests itself rather than trusting the maker's claim that "it works."
4. **The checker must actually discriminate** — a checker that passes everything isn't a checker. This project proves the reviewer catches a bad fix (`FAIL`, with reasons) and not just a good one (`PASS`).
5. **Human gate stays intact** — a real version of this loop would only open a pull request on `PASS`; a `FAIL` verdict goes to a human to look at, never straight to `main`.

## Requirements

* Git Bash (or another bash-compatible shell) on Windows
* Claude Code CLI installed and logged in
* Python 3.x with `pytest` installed

## Project Structure

This is a throwaway learning project. The reviewer subagent (`.claude/agents/reviewer.md`) and skill (`.claude/skills/fix-loop/`) are the reusable parts — the worktrees created during testing were temporary and removed once both verdicts were confirmed.

## Key Lesson

A checker is only trustworthy if it can fail something. Testing it against a deliberately bad fix — not just a good one — is what proves the maker-checker split actually works, rather than the reviewer simply agreeing with whatever the implementer says.
