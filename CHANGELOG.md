# Changelog

## [v0.2.2] - 2026-06-14

- refactor: revert to simple release flow, remove PR-based approach

## [v0.2.1] - 2026-06-14

- fix: force push release branch, handle existing PR
- fix: pass PR branch ref via env var in release-finalize
- fix: remove blank lines in create-release-pr action
- feat: two-phase release via PR (create-release-pr action)
- fix: add actions: read permission to release job

## [v0.2.0] - 2026-06-14

Replace `release-shared.yml` reusable workflow with four composable composite actions: `verify-release`, `generate-notes`, `commit-changelog`, `create-release`. Each action handles one concern and can be used independently. `baseline/release.yml` uses relative action refs to avoid self-reference pinning issues.

## [v0.1.1] - 2026-06-14

Release workflow switched to `workflow_dispatch` trigger with `release-shared.yml` reusable workflow. The shared release workflow now also bumps `version` in `pyproject.toml` (if present) as part of the changelog commit, enabling Homebrew-compatible Python packages.

## [v0.1.0] - 2026-06-14

Added `release-shared.yml` reusable workflow implementing the CI-owned release process: verifies base SHA, checks CI, generates AI release notes, commits changelog, creates tag and GitHub Release. Stripped CHANGELOG mutation from the `create-release` composite action.

## [v0.0.14] - 2026-06-13

- document separate artifact upload after create-release
- chore: update changelog for v0.0.13

## [v0.0.13] - 2026-06-13

- remove artifact-path from create-release action
- rename self-calling workflows to -self suffix; add dependabot-automerge-self; document convention
- add pre-commit config and self-update workflow
- restore telegram-release-notify reusable workflow; add notify-release for baseline self
- add dependabot and telegram-release-notify workflows
- document default schedules and pre-commit autoupdate in README
- chore: update changelog for v0.0.12

## [v0.0.12] - 2026-06-13

- add pre-commit-autoupdate reusable workflow
- use VERSION placeholder instead of pinned version in README
- update README and AGENTS.md with reusable workflows and current version
- chore: update changelog for v0.0.11

## [v0.0.11] - 2026-06-13

- fix changelog trailing newline in create-release action
- remove latest mutable tag from create-release action
- chore: update changelog for v0.0.10

## [v0.0.10] - 2026-06-13

- fix CHANGELOG (last manual fix — action is now patched)
- fix changelog update to preserve # Changelog header position
- chore: update changelog for v0.0.9

## [v0.0.9] - 2026-06-13

- fix changelog update to preserve # Changelog header position
- rename workflows to dependabot-automerge and telegram-release-notify
- fix CHANGELOG structure after merge conflict
- install shellcheck from stable release to get --rcfile support
- fix yamllint empty-lines violations
- add dependabot-automerge and telegram-release-notify reusable workflows
- add UP, B, SIM rules to ruff config

## [v0.0.6] - 2026-06-12

- replace linter reusable workflows with composite actions

## [v0.0.5] - 2026-06-12

- extract create-release composite action, remove publish-app-bundle

## [v0.0.3] - 2026-06-12

- add publish-app-bundle action and AI-generated release notes
