# AGENTS.md

This file provides guidance to AI coding agents when working with this repository.

## Message Prefix

Prefix every user-visible agent message with the agent emoji followed by the
repository name in square brackets:

`EMOJI [OWNER/REPO]:`

Replace `OWNER/REPO` with the current GitHub repository name.

Use the emoji to identify the agent:

- `🤖` Codex
- `🧠` Claude Code
- `🖊️` Cursor
- `🧩` unknown or other agent

This applies to chat replies, PR comments, review comments, issue comments,
status updates, and any other written communication.

## Purpose

This repo is the single source of truth for linter configs across all dupmachine repositories. The goal is identical linting everywhere — configs live here and nowhere else.

Baseline owns linter configuration, not runtime or tool installation. Consuming
repositories must install the runtimes and linter binaries they choose to run;
baseline hooks and actions should only pass canonical configs to already
installed tools.

## Repository Structure

- `config/` — canonical linter config files
- `hooks/` — shell script wrappers for pre-commit (`language: script`)
- `baseline.gemspec` — Ruby gem packaging RuboCop and erb_lint configs for local `bundle exec rubocop`
- `lib/` — gem code (`Baseline::VERSION`, install stubs)
- `exe/baseline-install` — writes project `.rubocop.yml` and `.erb_lint.yml` stubs
- `.github/actions/lint-*/` — thin composite actions that run installed linters with baseline configs
- `.github/actions/setup-runtimes/` — baseline self-lint only: installs runtimes and gems before lint actions
- `.github/workflows/lint.yml` — baseline self-lint (uses local actions, not `@vX`)
- `.github/workflows/prepare-release.yml` — dispatch workflow: calls `rubykatzen/releaser` to prepare `release/vX.Y.Z`
- `.github/workflows/publish-release.yml` — publishes merged `release/*` PRs via `rubykatzen/releaser`
- `.github/workflows/merge-dependabot-pr.yml` — baseline's own caller (delegates to `rubykatzen/releaser`)
- `.github/workflows/notify-telegram-unreleased.yml` — baseline's own caller (delegates to `rubykatzen/releaser`)
- `.pre-commit-hooks.yaml` — hook definitions for pre-commit
- `.pre-commit-config.yaml.example` — example for consuming repos

## Adding a New Linter

To add a linter for a new file type:

1. Add config to `config/<linter>.ext`
2. Add `hooks/<linter>.sh` — shell wrapper that passes the config path via `$(dirname "$0")/../config/<linter>.ext`
3. Make the script executable: `chmod +x hooks/<linter>.sh`
4. Add hook entry to `.pre-commit-hooks.yaml`
5. Add composite action to `.github/actions/lint-<linter>/action.yml`
6. Update `.pre-commit-config.yaml.example`
7. Update `README.md`
8. If any rules are disabled, add them to `LINTERS-DEFAULTS-OVERRIDES.md`

Do not make baseline install the linter runtime or binary. Document the required
tool and keep installation in the consuming repository's workflow or developer
environment.

## Workflows

`merge-dependabot-pr.yml` and `notify-telegram-unreleased.yml` are baseline's own
callers that delegate to `rubykatzen/releaser`; they are not exported for
external use.

Pre-commit hook pins in `.pre-commit-config.yaml` are updated by Dependabot
(`package-ecosystem: pre-commit` in `.github/dependabot.yml`), not by a custom
workflow.

## Self-linting

Baseline lints itself through `.github/workflows/lint.yml`, which calls the
shared reusable workflow `.github/workflows/lint-shared.yml`. Do not point the
baseline self-lint workflow at `rubykatzen/baseline@vX`; it must validate the
actions and configs from the current commit.

`main` branch protection requires the GitHub Actions status check named `lint / lint`.
That name comes from the `lint` job in `lint.yml` calling the `lint` job in
`lint-shared.yml`. If either job name changes, update branch protection in GitHub
at the same time.

## Cutting Releases

Use the [rubykatzen/releaser](https://github.com/rubykatzen/releaser) CLI.
Run from inside this repository:

```bash
releaser patch   # or: releaser minor / releaser major
```

The CLI does the following automatically:

1. Fetches `origin/main` and finds the latest SemVer tag
2. Verifies CI is green on `origin/main`
3. Calculates the next version
4. Dispatches `.github/workflows/prepare-release.yml` with the computed version
   and `base_sha`
5. Watches the workflow run
6. Opens a PR from `release/vX.Y.Z` → `main` and enables auto-merge

`.github/workflows/publish-release.yml` fires automatically once the PR merges
and creates the annotated tag and GitHub release.

To check readiness without triggering a release:

```bash
releaser status
releaser patch --dry-run
```

If the CLI is not installed: `brew tap rubykatzen/tap && brew install releaser`.

## Linter Selection

For language-agnostic file types (YAML, Markdown, shell, etc.), always choose the linter implemented in the highest-priority runtime:

Priority order: Python > TypeScript > everything else.

This avoids introducing new runtimes into repos that don't already use them.

## Disabled Rules

Rules are disabled only when impractical across all repos, not to accommodate a single repo. Per-repo overrides are not supported by design. Deviations from defaults are documented in `LINTERS-DEFAULTS-OVERRIDES.md`.
