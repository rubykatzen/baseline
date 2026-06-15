# AGENTS.md

This file provides guidance to AI coding agents when working with this repository.

## Purpose

This repo is the single source of truth for linter configs across all dupmachine repositories. The goal is identical linting everywhere — configs live here and nowhere else.

## Repository Structure

- `configs/` — canonical linter config files
- `hooks/` — shell script wrappers for pre-commit (`language: script`)
- `.github/actions/lint-*/` — composite actions, one per linter
- `.github/workflows/lint.yml` — baseline self-lint (uses local actions, not `@vX`)
- `.github/workflows/prepare-release.yml` — dispatch workflow: calls `rubykatzen/releaser` to prepare `release/vX.Y.Z`
- `.github/workflows/publish-release.yml` — publishes merged `release/*` PRs via `rubykatzen/releaser`
- `.github/workflows/dependabot-automerge-shared.yml` — **reusable**: merges Dependabot PRs immediately
- `.github/workflows/pre-commit-autoupdate-shared.yml` — **reusable**: runs `pre-commit autoupdate` and commits
- `.github/workflows/telegram-release-notify-shared.yml` — **reusable**: checks main CI + unreleased commits, notifies Telegram
- `.github/workflows/dependabot-automerge.yml` — baseline's own caller
- `.github/workflows/pre-commit-autoupdate.yml` — baseline's own caller
- `.github/workflows/telegram-release-notify.yml` — baseline's own caller
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

## Naming convention: `-shared` suffix for reusable workflows

Reusable (`workflow_call`) implementations carry a `-shared` suffix. Baseline's
own calling workflows and consumer repo workflows use the natural name without suffix:

| Reusable (baseline only) | Calling workflow (baseline + all consumers) |
|---|---|
| `dependabot-automerge-shared.yml` | `dependabot-automerge.yml` |
| `pre-commit-autoupdate-shared.yml` | `pre-commit-autoupdate.yml` |
| `telegram-release-notify-shared.yml` | `telegram-release-notify.yml` |

Consumer repos call the `-shared` variant:
`uses: rubykatzen/baseline/.github/workflows/dependabot-automerge-shared.yml@vX`

This keeps consumer workflow files conventionally named while making it obvious
in baseline which files are meant for external use.

## Self-linting

Baseline lints itself through `.github/workflows/lint.yml` using local composite
actions (`./.github/actions/lint-*`). Do not point the baseline self-lint
workflow at `rubykatzen/baseline@vX`; it must validate the actions and
configs from the current commit.

`main` branch protection requires the GitHub Actions status check named `lint`.
That name comes from the `lint` job in `.github/workflows/lint.yml`; if the job
name changes, update branch protection in GitHub at the same time.

## Cutting Releases

Baseline releases are cut with `rubykatzen/releaser`, not with release logic
maintained in this repo. To prepare a release, dispatch
`.github/workflows/prepare-release.yml` on `main` with:

- `version`: new version without `v` prefix, for example `0.4.4`
- `base_sha`: current `origin/main` SHA, used by releaser's verify step to avoid
  preparing from a stale branch

The prepare workflow creates and pushes `release/vX.Y.Z` with an updated
`CHANGELOG.md`. Open a PR from that branch to `main`; after it is reviewed and
merged, `.github/workflows/publish-release.yml` reads the release data from the
merged branch and creates the `vX.Y.Z` tag and GitHub release.

## Linter Selection

For language-agnostic file types (YAML, Markdown, shell, etc.), always choose the linter implemented in the highest-priority runtime:

Priority order: Python > TypeScript > everything else.

This avoids introducing new runtimes into repos that don't already use them.

## Disabled Rules

Rules are disabled only when impractical across all repos, not to accommodate a single repo. Per-repo overrides are not supported by design. Deviations from defaults are documented in `README.md`.
