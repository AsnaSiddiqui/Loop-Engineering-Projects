---
name: fix-loop
description: >-
  Drafts a fix for one bug in an isolated worktree, then asks the reviewer
  subagent to grade it PASS or FAIL before anything is finalized.
---

# Fix loop

1. Read the failing test to understand what correct behavior looks like.
2. Create an isolated worktree on a new branch named `claude/<short-slug>`.
3. Draft the smallest fix that makes the failing test(s) pass. Do not change
   anything else.
4. Run the tests yourself and confirm they pass before asking for review.
5. Ask the reviewer subagent to grade the diff. Wait for its verdict.
6. If PASS: report that this fix is ready to open as a PR.
7. If FAIL: report the reviewer's reasons and stop. Do not retry silently.
