# Changelog

## [Unreleased]

## [v0.6.1] - 2026-06-20

- chore: bump releaser to v0.4.5
- chore: bump releaser to v0.4.4, drop manual Gemfile.lock step
- fix: update Gemfile.lock when bumping gem version on release branch

## [v0.6.0] - 2026-06-20

- refactor: require baseline gem for ruby linting (#47)

## [v0.5.4] - 2026-06-19

- feat: publish baseline Ruby gem with RuboCop and erb_lint configs
- feat: comment out todo inherit_from in install stubs with generation hints
- fix: skip gem-delegating rubocop and erb_lint hooks when no target files
- fix: remove stale gem artifacts before RubyGems publish
- fix: silence RuboCop extension suggestions in shared config
- fix: generate `.erb_lint.yml` stub instead of deprecated `.erb-lint.yml`
- fix: pin RuboCop 1.88+ to match standard config parameters

## [v0.5.3] - 2026-06-19

- lint: disable pymarkdown pragma suppressions (#51)
- erb-lint: skip vendor with project config (#45)

## [v0.5.2] - 2026-06-18

- lint: allow markdown fragments without h1 (#49)
- chore(deps): bump actions/checkout from 6 to 7
- fix: disable frozen string comments for erb lint (#46)
- docs: add portable agent message prefix

## [v0.5.1] - 2026-06-17

- refactor: move bump-pre-commit-rev into local composite action
- feat: bump pre-commit rev in prepare-release, drop Dependabot pre-commit ecosystem
- chore(deps): bump https://github.com/rubykatzen/baseline
- fix: remove stale conflict marker from README
- Replace pre-commit autoupdate workflow with Dependabot.
- docs: add erb_lint todo file format and creation instructions
- fix: inherit baseline rubocop config inside erb_lint rubocop_config
- fix: pin transitive gem dependencies to minor versions in gemspec
- fix: use HTTPS URLs in pre-commit configs for Dependabot compatibility

## [v0.5.0] - 2026-06-17

- chore: bump releaser to v0.3.4
- fix: remove trailing comma after last hash item in Install::STUBS
- fix: address PR review for gem hooks, gemspec, and publish
- feat: comment todo inherit_from in install stubs with hints
- fix: address PR review blockers for rubykatzen-baseline gem
- feat: enable Style/FrozenStringLiteralComment
- rename configs/ to config/ to follow Ruby gem conventions
- rename configs/erb-lint.yml to configs/erb_lint.yml for consistency
- feat: publish rubykatzen-baseline gem on release
- rename gem to rubykatzen-baseline
- chore: bump releaser to v0.3.3, add bump-ruby-gem-version to release flow
- fix: drop erb_lint version pin — it depends on rubocop >= 1 internally
- fix: drop version pins for rubocop-* and standard-custom
- fix: tighten gem pins to minor version constraints
- fix: check .erb_lint.yml (not deprecated .erb-lint.yml), loosen gem pins
- docs: note RuboCop version pins in changelog
- fix: pin RuboCop 1.88+ and rubocop-rails 2.35+ in baseline gem
- fix: silence RuboCop extension tips in shared config
- fix: use MaximumRangeSize in standard rubocop config
- feat: publish baseline Ruby gem for RuboCop and erb_lint configs

## [v0.4.10] - 2026-06-16

- feat: inline standard rubocop configs, drop standard gem wrappers (#30)

## [v0.4.9] - 2026-06-16

- fix: make hooks/herb.sh executable (#27)

## [v0.4.8] - 2026-06-16

- setup-ruby: enable bundler cache when Gemfile is present (#24)

## [v0.4.7] - 2026-06-16

- herb: add lint-herb action (#22)

## [v0.4.6] - 2026-06-16

- erb-lint: use find to collect files, drop --lint-all (#20)

## [v0.4.5] - 2026-06-16

- erb-lint: exclude vendor from linting (#18)
- Update README to generalize workflow description
- chore: remove release actions moved to rubykatzen/releaser (#17)

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
