# AGENTS.md

This file provides guidance to AI coding agents when working with this repository.

<!-- baseline fragment: message-prefix -->
## Message Prefix

Prefix every user-visible agent message with the agent emoji followed by the
repository name in square brackets:

`EMOJI [OWNER/REPO]:`

Replace `OWNER/REPO` with the current GitHub repository name.

Use the emoji to identify the agent:

- `🤖` Codex
- `🧠` Claude Code
- `🖱️` Cursor
- `🥽` GitHub Copilot
- `🧩` unknown or other agent

This applies to chat replies, PR comments, review comments, issue comments,
status updates, and any other written communication.
<!-- /baseline fragment: message-prefix -->

<!-- baseline fragment: message-suffix -->
## Message Suffix

End every user-visible agent message with a blank line followed by a final
line containing exactly three emoji relevant to the message context:

`EMOJI EMOJI EMOJI`
<!-- /baseline fragment: message-suffix -->

<!-- baseline fragment: embedded-fragments -->
## Embedded Fragments

This repository uses [Baseline](https://github.com/rubykatzen/baseline) to
verify shared content fragments across repositories.

Do not change a required fragment only in the consuming repository. Change
the fragment in `config/embedder.yml` in Baseline and release it. Dependabot
will then update the Baseline workflow version in consuming repositories and
CI will show the required fragment diff.

A repository-specific exception must be declared through the `skip` input of
`embedder-shared.yml`.
<!-- /baseline fragment: embedded-fragments -->

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
- `.github/actions/check-embedder/` — validates required content fragments in consumer files
- `.github/actions/detect-linters/` — composite action that selects applicable linters from tracked files
- `.github/actions/check-precommit/` — composite action: verifies pre-commit hooks match detected CI linters
- `.github/actions/setup-runtimes/` — installs Python packages, Ruby, and standalone binaries for requested linters; Python is provided by the runner
- `.github/actions/prepare-telegram-pr-message/` — formats pull request and open-PR digest messages
- `.github/actions/prepare-telegram-issue-message/` — formats closed-issue messages
- `.github/actions/send-telegram-message/` — sends plain-text messages through the Telegram Bot API
- `.github/workflows/lint-shared.yml` — reusable workflow exported for consuming repos: setup + lint
- `.github/workflows/embedder-shared.yml` — reusable workflow exported for required content validation
- `.github/workflows/notify-telegram-pr-shared.yml` — reusable pull request notifications and open-PR digest
- `.github/workflows/notify-telegram-issue-shared.yml` — optional reusable issue-closure notifications
- `.github/workflows/pr.yml` — validates Baseline pull request titles against Conventional Commits
- `.github/workflows/lint.yml` — baseline self-lint (uses local `./` references, not `@vX`)
- `.github/workflows/release-please.yml` — maintains the release PR and publishes merged releases
- `.github/workflows/notify-telegram-pr.yml` — Baseline's own Telegram pull request notification caller
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
7. Add a step to `.github/workflows/lint-shared.yml` gated on `contains(fromJSON(steps.detect.outputs.linters), '<key>')`
8. Update `.pre-commit-config.yaml.example`
9. Update `README.md`
10. If any rules are disabled, add them to `LINTERS-DEFAULTS-OVERRIDES.md`

Do not make baseline install the linter runtime or binary in pre-commit hooks.
Pre-commit hooks expect tools to already be on PATH in the developer environment.
`setup-runtimes` handles installation for CI only (called from `lint-shared.yml`).

## Workflows

`notify-telegram-pr-shared.yml` exports pull request notifications and the
open-pull-request digest. Baseline calls it locally through
`notify-telegram-pr.yml`.

`notify-telegram-issue-shared.yml` exports optional issue-closure notifications.
The caller owns any label or other notification condition; the shared workflow
does not modify issues. Baseline does not call it because this repository does
not use issue notifications.

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

Release Please maintains a release pull request from Conventional Commits on
`main`. Review the proposed version, changelog, and file updates, then merge the
pull request to release. The workflow creates the version tag and GitHub
Release, publishes the gem, and updates the floating major and minor tags.

The workflow requires a fine-grained personal access token in the
`RELEASE_TOKEN` repository secret, limited to this repository with read
and write access to contents, issues, and pull requests. The token ensures
release pull requests trigger required CI.

## Linter Selection

For language-agnostic file types (YAML, Markdown, shell, etc.), always choose the linter implemented in the highest-priority runtime:

Priority order: Python > TypeScript > everything else.

This avoids introducing new runtimes into repos that don't already use them.

## Disabled Rules

Rules are disabled only when impractical across all repos, not to accommodate a single repo. Per-repo overrides are not supported by design, except for Tombi, which intentionally discovers the consumer repository's configuration. Deviations from defaults are documented in `LINTERS-DEFAULTS-OVERRIDES.md`.
