---
name: daily-freshness-check
description: >-
  Checks README freshness across sibling project folders (read-only) and
  reports findings, without ever modifying anything outside this project's
  own folder.
---

# Daily freshness check

1. Read `progress.md` in this folder first, to see what was already found
   in previous runs.
2. Using the Read tool ONLY (never Edit or Write) on any folder outside
   this one, check each sibling `project_0X_*` folder for:
   - Does `README.md` exist?
   - Does it contain a "Key Lesson" section?
   - Is it suspiciously short (under 20 lines)?
3. Budget guard: check at most 10 project folders per run, and stop if the
   run has read more than 30 files total.
4. Write or update `freshness_report.md` in THIS folder only, summarizing
   findings per project.
5. Update `progress.md` in THIS folder: add a dated entry noting what was
   checked and what (if anything) needs human attention.
6. Draft this work on an isolated worktree branch. Ask the reviewer
   subagent to grade the diff PASS or FAIL.
7. On PASS: open a PR with the updated report. On FAIL: leave a
   "needs a human" note in progress.md and do not open a PR.

**Hard rule:** Never use Edit or Write on any file outside
`project_08_your_own_daily_loop/`. If tempted to fix something you find in
another project, do not — only report it.
