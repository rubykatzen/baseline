# Changelog

## [v0.4.4] - 2026-06-15

- docs: replace manual workflow dispatch with releaser CLI in release docs
- docs: add concrete release command example to AGENTS.md
- docs: add link to rubykatzen/releaser in AGENTS.md
- docs: remove dependabot-automerge and telegram workflows from public docs
- Skip hooks when no targets exist (#15)
- docs: document release flow and branch protection
- fix: use relative path for pre-commit-autoupdate shared workflow
- fix portable sed in mise.toml parsing, trap cleanup, and README accuracy
- simplify Ruby linting: setup-ruby handles bundle install, linters detect Gemfile
- chore(deps): bump rubykatzen/baseline/.github/workflows/pre-commit-autoupdate-shared.yml
- use bundle install in Ruby linter actions, remove BASELINE_RUBY_LINTER_STANDALONE
- extract setup-ruby action and add guard steps to Ruby linters
- chore(deps): bump rubykatzen/releaser from 0.3.0 to 0.3.1
- rubocop: exclude vendor from linting
- make Ruby linter actions self-contained

## [v0.4.3] - 2026-06-15

- fix Ruby pre-commit hook file handling

## [v0.4.2] - 2026-06-15

- add Ruby linters: rubocop and erb-lint

## [v0.4.1] - 2026-06-15

- chore: reference telegram-notify and dependabot-automerge from rubykatzen/releaser@v0.3.1

## [v0.4.0] - 2026-06-15

- feat: move release actions to releaser, reference rubykatzen/releaser@v0.3.0

## [v0.3.0] - 2026-06-15

- fix: remove blank lines in read-release-data to pass yamllint
- feat: PR-based release flow with composable actions

## [v0.2.3] - 2026-06-14

- refactor: split pyproject version bump into separate action

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
