# AGENTS.md

This file provides guidance to AI coding agents when working with this repository.

## Purpose

This repo is the single source of truth for linter configs across all dupmachine repositories. The goal is identical linting everywhere — configs live here and nowhere else.

## Repository Structure

- `configs/` — canonical linter config files
- `hooks/` — shell script wrappers for pre-commit (`language: script`)
- `.github/actions/lint-*/` — composite actions, one per linter
- `.github/actions/create-release/` — composite action: publish release, AI notes, update CHANGELOG
- `.github/workflows/lint.yml` — baseline self-lint (uses local actions, not `@vX`)
- `.github/workflows/release.yml` — cuts baseline releases via `create-release` action
- `.github/workflows/dependabot-automerge.yml` — **reusable**: merges Dependabot PRs immediately
- `.github/workflows/pre-commit-autoupdate.yml` — **reusable**: runs `pre-commit autoupdate` and commits
- `.github/workflows/telegram-release-notify.yml` — **reusable**: checks main CI + unreleased commits, notifies Telegram
- `.github/workflows/dependabot-automerge-self.yml` — baseline's own caller (see `-self` convention below)
- `.github/workflows/pre-commit-autoupdate-self.yml` — baseline's own caller
- `.github/workflows/telegram-release-notify-self.yml` — baseline's own caller
- `.pre-commit-hooks.yaml` — hook definitions for pre-commit
- `.pre-commit-config.yaml.example` — example for consuming repos

## Adding a New Linter

To add a linter for a new file type:

1. Add config to `configs/<linter>.ext`
2. Add `hooks/<linter>.sh` — shell wrapper that passes the config path via `$(dirname "$0")/../configs/<linter>.ext`
3. Make the script executable: `chmod +x hooks/<linter>.sh`
4. Add hook entry to `.pre-commit-hooks.yaml`
5. Add composite action to `.github/actions/lint-<linter>/action.yml`
6. Update `.pre-commit-config.yaml.example`
7. Update `README.md`

## Reusable workflows

`dependabot-automerge.yml`, `pre-commit-autoupdate.yml`, and
`telegram-release-notify.yml` are `workflow_call` workflows consumed by other
repos. When editing them, test by dispatching from a consumer repo.

`telegram-release-notify.yml` requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
secrets in the calling repo. It checks the latest `lint.yml` run on `main` and
the number of commits since the last semver tag.

## Self workflows (`-self` suffix)

Baseline's own scheduled/triggered workflows are named with a `-self` suffix to
distinguish them from the reusable implementations that share the same directory:

| File | Calls |
|---|---|
| `dependabot-automerge-self.yml` | `dependabot-automerge.yml` |
| `pre-commit-autoupdate-self.yml` | `pre-commit-autoupdate.yml` |
| `telegram-release-notify-self.yml` | `telegram-release-notify.yml` |

This suffix convention is baseline-specific. Consumer repos use conventional names
(e.g. `dependabot-automerge.yml`) because they only contain the calling side.

## Self-linting

Baseline lints itself through `.github/workflows/lint.yml` using local composite
actions (`./.github/actions/lint-*`). Do not point the baseline self-lint
workflow at `rubykatzen/baseline@vX`; it must validate the actions and
configs from the current commit.

## Linter Selection

For language-agnostic file types (YAML, Markdown, shell, etc.), always choose the linter implemented in the highest-priority runtime:

Priority order: Python > TypeScript > everything else.

This avoids introducing new runtimes into repos that don't already use them.

## Disabled Rules

Rules are disabled only when impractical across all repos, not to accommodate a single repo. Per-repo overrides are not supported by design. Deviations from defaults are documented in `README.md`.
