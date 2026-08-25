# Loop Engineering Projects

A collection of hands-on projects built while learning **Loop Engineering** from *The AI Agent Factory* book — the shift from prompting an agent step-by-step to designing a system that runs on its own: a heartbeat that starts it, a body that does the work, and a spine that remembers between runs.

## What's in this repo

Each project lives in its own folder, numbered in the order it was built.

Every project folder has its own `README.md` explaining:

* what that project demonstrates
* which loop-engineering concept it uses (heartbeat type, checker, spine, etc.)
* exact steps to run it
* what "done" looks like
* the key lesson learned

New projects are added over time as the course progresses — check each project's own `README.md` for details on what it covers.

## Structure

```text
loop_engineering_projects/
├── project_01_.../
├── project_02_.../
├── project_03_.../
├── ...
└── README.md          ← this file
```

## Common Setup Used Across Projects

* **Claude Code CLI** as the agent runtime
* **Git Bash** as the shell (Windows)
* **Python 3.x** with `pytest` for projects involving tests
* Each project is a throwaway learning sandbox — not production code

## Concepts Covered So Far

Loop engineering is built around a few core ideas. Each project focuses on one or more of these:

* **Heartbeats** — what starts a loop: in-session, conditional, scheduled, or event-driven
* **The body** — what the loop actually does on each run
* **The spine** — how a loop remembers what happened in previous runs (usually a plain Markdown file it reads first and updates last)
* **Maker-checker** — separating the agent that does the work from the agent that grades it, so the work is verified independently rather than self-reported
* **Skills and worktrees** — packaging repeatable steps and isolating parallel work safely

## Notes

This is a personal learning repository, following the project exercises laid out in the Loop Engineering crash course.

Code and setups here are intentionally simple and disposable — the goal is understanding the loop patterns, not production-quality software.
