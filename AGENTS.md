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

This repo is the single source of truth for linter configs across all rubykatzen repositories. The goal is identical linting everywhere — configs live here and nowhere else.

Baseline owns linter configuration and runtime installation for CI. Consuming
repositories call `lint-shared.yml` and get runtimes, configs, and linter
execution handled automatically. Pre-commit hooks are thin wrappers that expect
tools to already be installed in the developer environment.

## Repository Structure

- `config/` — canonical linter config files
- `hooks/` — shell and Python script wrappers for pre-commit (`language: script`)
- `baseline.gemspec` — Ruby gem packaging RuboCop and erb_lint configs for local `bundle exec rubocop`
- `lib/` — gem code (`Baseline::VERSION`, install stubs)
- `exe/baseline-install` — writes project `.rubocop.yml` and `.erb_lint.yml` stubs
- `.github/actions/lint-*/` — composite actions that run installed linters with baseline configs
- `.github/actions/check-precommit-sync/` — composite action: checks coverage and CI/pre-commit sync
- `.github/actions/setup-runtimes/` — installs Python, Ruby, and standalone binaries for requested linters
- `.github/workflows/lint-shared.yml` — reusable workflow exported for consuming repos: setup + lint
- `.github/workflows/lint.yml` — baseline self-lint (uses local `./` references, not `@vX`)
- `.github/workflows/prepare-release.yml` — dispatch workflow: calls `rubykatzen/releaser` to prepare `release/vX.Y.Z`
- `.github/workflows/publish-release.yml` — publishes merged `release/*` PRs via `rubykatzen/releaser`
- `.github/workflows/notify-telegram-unreleased.yml` — baseline's own caller (delegates to `rubykatzen/releaser`)
- `.pre-commit-hooks.yaml` — hook definitions for pre-commit
- `.pre-commit-config.yaml.example` — example for consuming repos (all hooks, prune as needed)

## Adding a New Linter

To add a linter for a new file type:

1. Add config to `config/<linter>.ext`
2. Add `hooks/<linter>.sh` — shell wrapper that passes the config path via `$(dirname "$0")/../config/<linter>.ext`
3. Make the script executable: `chmod +x hooks/<linter>.sh`
4. Add hook entry to `.pre-commit-hooks.yaml`
5. Add composite action to `.github/actions/lint-<linter>/action.yml`
6. Add runtime installation to `.github/actions/setup-runtimes/action.yml`
7. Add a step to `.github/workflows/lint-shared.yml` gated on `contains(inputs.linters, '<key>')`
8. Update `.pre-commit-config.yaml.example`
9. Update `README.md`
10. If any rules are disabled, add them to `LINTERS-DEFAULTS-OVERRIDES.md`

Do not make baseline install the linter runtime or binary in pre-commit hooks.
Pre-commit hooks expect tools to already be on PATH in the developer environment.
`setup-runtimes` handles installation for CI only (called from `lint-shared.yml`).

## Workflows

`notify-telegram-unreleased.yml` is baseline's own caller that delegates to
`rubykatzen/releaser`; it is not exported for external use.

`lint-shared.yml` is the primary export — consuming repos call it via
`uses: rubykatzen/baseline/.github/workflows/lint-shared.yml@VERSION`.

Pre-commit hook pins in `.pre-commit-config.yaml` are updated by Dependabot
(`package-ecosystem: pre-commit` in `.github/dependabot.yml`), not by a custom
workflow.

## Self-linting

Baseline lints itself through `.github/workflows/lint.yml`, which calls the
shared reusable workflow `.github/workflows/lint-shared.yml` using a local
`./` reference. This ensures the current commit's actions and configs are
validated, not a pinned release.

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
