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

<!-- baseline fragment: no-emoji-in-docs -->
## No Emoji in Documentation

Do not use emoji in documentation or README content, including headings,
prose, lists, and code comments. This applies to `README.md`, `AGENTS.md`,
and any other Markdown documentation in the repository.

This does not apply to the Message Prefix and Message Suffix conventions
above, which require emoji in written agent communication.
<!-- /baseline fragment: no-emoji-in-docs -->

<!-- baseline fragment: embedded-fragments -->
## Embedded Fragments

This repository uses [Baseline](https://github.com/rubykatzen/baseline) to
verify shared content fragments across repositories.

Do not change a required fragment only in the consuming repository. Change
the fragment in `config/embedder.yml` or the selected extra configuration in
Baseline and release it. Dependabot will then update the Baseline workflow
version in consuming repositories and CI will show the required fragment
diff.

A repository-specific exception must be declared through the `skip` input of
`embedder-shared.yml`. Optional policies are selected through its `extra`
input.
<!-- /baseline fragment: embedded-fragments -->

## Purpose

Baseline is the centrally managed source of development policy for repositories
across organizations and programming language stacks. Its goal is a
zero-configuration, homogeneous development experience for developers who move
between stacks.

Baseline owns linter configuration and CI runtime installation, GitHub repository
policy, required content fragments, and reusable notification workflows.
Consumers connect only the workflows they need. Checks verify policy but do not
mutate consumer repositories; intentional differences use explicit `skip`
inputs. Pre-commit hooks are thin wrappers that expect tools to already be
installed in the developer environment.

## Repository Structure

- `config/` — canonical linter, GitHub policy, and Embedder configuration
- `hooks/` — shell and Python script wrappers for pre-commit (`language: script`)
- `baseline.gemspec` — Ruby gem packaging RuboCop, erb_lint, and Herb tooling
- `lib/` — gem code (`Baseline::VERSION`, install stubs)
- `exe/baseline-install` — writes project `.rubocop.yml` and `.erb_lint.yml` stubs
- `.github/actions/lint-*/` — composite actions that run installed linters with baseline configs
- `.github/actions/check-embedder/` — validates base and named extra content fragments
- `.github/actions/check-github-config/` — validates repository settings and labels
- `.github/actions/detect-linters/` — composite action that selects applicable linters from tracked files
- `.github/actions/check-precommit/` — composite action: verifies pre-commit hooks match detected CI linters
- `.github/actions/setup-runtimes/` — installs Python packages, Ruby, and standalone binaries for requested linters; Python is provided by the runner
- `.github/actions/*telegram*/` — prepares and sends Telegram notifications
- `.github/workflows/*-shared.yml` — reusable workflows exported to consumers
- `.github/workflows/lint.yml`, `github.yml`, and `embedder.yml` — local self-check callers
- `.github/workflows/pr.yml` — validates Baseline pull request titles against Conventional Commits
- `.github/workflows/release.yml` — maintains the release PR and publishes merged releases
- `.github/workflows/notify-telegram-pr.yml` and `notify-telegram-release.yml` — Baseline's own Telegram notification callers
- `.github/workflows/test.yml` — runs the Python test suite
- `.pre-commit-hooks.yaml` — hook definitions for pre-commit

## Adding a New Linter

To add a linter for a new file type:

1. Add config to `config/<linter>.ext`
2. Add `hooks/<linter>.sh` — shell wrapper that passes the config path via `$(dirname "$0")/../config/<linter>.ext`
3. Make the script executable: `chmod +x hooks/<linter>.sh`
4. Add hook entry to `.pre-commit-hooks.yaml`
5. Add composite action to `.github/actions/lint-<linter>/action.yml`
6. Add runtime installation to `.github/actions/setup-runtimes/action.yml`
7. Add a step to `.github/workflows/lint-shared.yml` gated on `contains(fromJSON(steps.detect.outputs.linters), '<key>')`
8. Update the pre-commit example in `README.md`
9. If any rules are disabled, add them to `LINTERS-DEFAULTS-OVERRIDES.md`

Do not make baseline install the linter runtime or binary in pre-commit hooks.
Pre-commit hooks expect tools to already be on PATH in the developer environment.
`setup-runtimes` handles installation for CI only (called from `lint-shared.yml`).

## Workflows

`lint-shared.yml` auto-detects applicable linters, installs their CI runtimes,
checks pre-commit synchronization when configured, and runs the canonical
tooling.

`github-shared.yml` verifies repository settings and labels against
`config/github.yml`. `embedder-shared.yml` verifies the base fragment set and
named configurations selected through its `extra` JSON input. Extra fragment
IDs use the `<configuration>/<fragment>` namespace in `skip`.

`notify-telegram-pr-shared.yml` exports pull request notifications and the
open-pull-request digest. Baseline calls it locally through
`notify-telegram-pr.yml`.

`notify-telegram-issue-shared.yml` exports optional issue-closure notifications.
The caller owns any label or other notification condition; the shared workflow
does not modify issues. Baseline does not call it because this repository does
not use issue notifications.

`notify-telegram-release-shared.yml` exports release publication notifications.
Baseline calls it locally through `notify-telegram-release.yml`.

Pre-commit hook pins in `.pre-commit-config.yaml` are updated by Dependabot
(`package-ecosystem: pre-commit` in `.github/dependabot.yml`), not by a custom
workflow.

## Self-validation

Baseline calls its lint, GitHub, and Embedder reusable workflows through local
`./` references. This validates the current commit's actions and configurations,
not a pinned release. The Embedder self-check enables the `release-please` extra
configuration.

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

This minimizes setup by preferring the Python runtime already present on GitHub
runners before introducing another toolchain.

## Disabled Rules

Rules are disabled only when impractical across all repos, not to accommodate a single repo. Per-repo overrides are not supported by design, except for Tombi, which intentionally discovers the consumer repository's configuration. Deviations from defaults are documented in `LINTERS-DEFAULTS-OVERRIDES.md`.
