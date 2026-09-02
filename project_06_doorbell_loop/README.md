# Project 06 — The Doorbell Loop

A project demonstrating an event-driven loop: a system that reacts to a
GitHub pull request automatically, with no prompt typed by a human.

## What This Project Does

A pull request is opened against this repo with a deliberately planted
bug in `shopping_cart.py`. The goal: get a code review to happen
automatically, triggered purely by the PR event — completing the fourth
and final heartbeat type (in-session, conditional, scheduled, and now
event-driven).

## Files

- `shopping_cart.py` — contains `calculate_total()` and `apply_tax()`
- `test_shopping_cart.py` — tests for both functions
- `.github/workflows/claude-review.yml` (at repo root) — the GitHub
  Actions workflow intended to trigger Claude automatically on PRs
  touching this folder

## How This Was Built

### Step 1: Baseline code and tests

Working code was committed to `main`, with passing tests confirmed via
`pytest`.

### Step 2: A real GitHub Actions workflow was set up

```yaml
name: Claude PR Review
on:
  pull_request:
    types: [opened, synchronize]
    paths:
      - 'project_06_doorbell_loop/**'
jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        env:
          ANTHROPIC_BASE_URL: https://openrouter.ai/api/v1
          ANTHROPIC_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
        with:
          prompt: |
            Review this pull request. Look for bugs, especially off-by-one
            errors, logic mistakes, or missing edge case handling. Leave
            your review as a comment on the PR.
```

An `OPENROUTER_API_KEY` secret was added via `gh secret set`, and the
Claude Code GitHub App was installed on the repo at
https://github.com/apps/claude.

### Step 3: A PR was opened with a planted bug

```bash
git checkout -b fix/tax-calculation-bug
```

`apply_tax()` was changed from the correct `amount * (1 + tax_rate)` to
the incorrect `amount * tax_rate` — a subtle logic bug that silently
returns only the tax portion instead of the total.

```bash
gh pr create --title "Update tax calculation" --base main --head fix/tax-calculation-bug
```

### Step 4: The cloud automation was debugged through three real issues

1. **Missing `id-token: write` permission** — the action failed to
   fetch an OIDC token without it. Fixed by adding the permission.
2. **Claude Code GitHub App not installed** — the action needs the app
   installed on the repo to exchange tokens. Fixed by installing it at
   github.com/apps/claude.
3. **OpenRouter SDK incompatibility** — after both fixes, the action
   authenticated correctly and installed Claude Code on the runner, but
   the actual model call failed immediately (`is_error: true`,
   `total_cost_usd: 0`, sub-second duration) when routed through
   OpenRouter. The `claude-code-action` SDK is built for Anthropic's
   direct API, and this specific compatibility issue could not be
   resolved without a direct Anthropic API key.

### Step 5: The review was completed locally instead

Since a direct Anthropic key wasn't available, the same diff was
reviewed locally with Claude Code (using the working local setup) and
the resulting review was posted to the PR manually via `gh pr comment`,
clearly labeled as a local simulation of the intended automated review.

## Result

The review correctly identified the planted bug: `apply_tax()` returns
only the tax amount instead of the total including tax, and
recommended rejecting the PR and reverting the change.

## Requirements

- Git Bash on Windows
- Claude Code CLI, logged in
- GitHub CLI (`gh`), authenticated
- Python 3.x with `pytest`
- A GitHub repository with Actions enabled

## Key Lesson

An event-driven loop needs its trigger (the PR event), its permissions
(`id-token: write`, the GitHub App), and a compatible model backend —
all three have to work together in a cloud environment with no local
fallback. Debugging three separate, real infrastructure issues here —
permissions, app installation, and provider compatibility — was itself
part of what "event-driven loop engineering" actually involves. When
the last piece (a direct-API-compatible key) wasn't available, falling
back to a local review and documenting that honestly is more valuable
than pretending full cloud automation succeeded when it didn't.
