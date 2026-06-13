# Changelog

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
