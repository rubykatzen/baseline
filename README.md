# Baseline

Shared linter configs, composite GitHub Actions, and reusable workflows for all rubykatzen/dupmachine repositories.

## Quick setup

Replace `VERSION` in all examples with the latest release tag from
[github.com/rubykatzen/baseline/releases](https://github.com/rubykatzen/baseline/releases).
After initial setup, [Dependabot](#2-dependabot) keeps the pin current automatically.

### 1. Lint workflow

Create `.github/workflows/lint.yml`. Include only the linters relevant to your stack:

```yaml
name: Lint
on:
  push:
    branches: ["main"]
  pull_request:
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: rubykatzen/baseline/.github/actions/lint-yamllint@VERSION
      - uses: rubykatzen/baseline/.github/actions/lint-pymarkdown@VERSION
      - uses: rubykatzen/baseline/.github/actions/lint-ruff@VERSION
      - uses: rubykatzen/baseline/.github/actions/lint-shellcheck@VERSION
      - uses: rubykatzen/baseline/.github/actions/lint-actionlint@VERSION
      - uses: rubykatzen/baseline/.github/actions/setup-ruby@VERSION
      - uses: rubykatzen/baseline/.github/actions/lint-rubocop@VERSION
      - uses: rubykatzen/baseline/.github/actions/lint-erb-lint@VERSION
```

Each action installs its own tool — no setup step needed. Ruby linter actions
require `setup-ruby` to run first; they will fail with a clear error if Ruby is
not in PATH.

### 2. Dependabot

Add `.github/dependabot.yml` to keep the version pin current automatically:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: daily
      time: "22:00"
      timezone: "Europe/Berlin"
```

### 3. Auto-merge Dependabot PRs (optional)

Create `.github/workflows/dependabot-automerge.yml`:

```yaml
name: Dependabot Automerge
on:
  pull_request_target:
    types: [opened, reopened, synchronize]
jobs:
  merge:
    uses: rubykatzen/baseline/.github/workflows/dependabot-automerge.yml@VERSION
    secrets: inherit
```

Merges all Dependabot PRs immediately without waiting for CI.

### 4. Pre-commit autoupdate (optional)

Create `.github/workflows/pre-commit-autoupdate.yml`:

```yaml
name: Pre-commit Autoupdate
on:
  schedule:
    - cron: "30 21 * * *"  # 22:30 Europe/Berlin (UTC+1)
  workflow_dispatch:
jobs:
  autoupdate:
    uses: rubykatzen/baseline/.github/workflows/pre-commit-autoupdate.yml@VERSION
    secrets: inherit
```

Runs `pre-commit autoupdate` daily and commits the result directly to `main`.

### 5. Telegram release notifications (optional)

Create `.github/workflows/telegram-release-notify.yml`.
Requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` secrets in the repo.

```yaml
name: Telegram Release Notify
on:
  schedule:
    - cron: "0 22 * * *"  # 23:00 Europe/Berlin (UTC+1)
  workflow_dispatch:
jobs:
  notify:
    uses: rubykatzen/baseline/.github/workflows/telegram-release-notify.yml@VERSION
    secrets: inherit
```

Sends a Telegram message when `main` is broken or has unreleased commits.
Cron schedule is configurable per repo.

---

## Composite actions (linters)

| Action | Lints | Config |
|---|---|---|
| `lint-yamllint` | `*.yml`, `*.yaml` | `configs/yamllint.yml` |
| `lint-pymarkdown` | `*.md` | `configs/pymarkdown.json` |
| `lint-ruff` | `*.py` | `configs/ruff.toml` |
| `lint-shellcheck` | `*.sh` | `configs/shellcheck.rc` |
| `lint-actionlint` | `.github/workflows/*.yml` | — |
| `lint-rubocop` | `*.rb` | `configs/rubocop.yml` |
| `lint-erb-lint` | `*.erb` | `configs/erb-lint.yml` |

## Reusable workflows

| Workflow | Trigger in caller | What it does |
|---|---|---|
| `dependabot-automerge.yml` | `pull_request_target` | Merges Dependabot PRs immediately |
| `pre-commit-autoupdate.yml` | `schedule` / `workflow_dispatch` | Runs `pre-commit autoupdate` and commits to main |
| `telegram-release-notify.yml` | `schedule` / `workflow_dispatch` | Notifies Telegram when main is broken or has unreleased commits |

## Releases

Baseline releases are cut with
[rubykatzen/releaser](https://github.com/rubykatzen/releaser), not with release
logic maintained in this repo. The local release workflows are thin callers:

- `.github/workflows/prepare-release.yml` dispatches releaser actions to verify
  `main`, generate notes, create `release/vX.Y.Z`, update `CHANGELOG.md`, and
  push the branch.
- `.github/workflows/publish-release.yml` runs after a merged `release/*` PR and
  uses releaser actions to read the release data, create the `vX.Y.Z` tag, and
  publish the GitHub release.

Patch release flow:

```bash
git fetch origin main --tags
base_sha=$(git rev-parse origin/main)
gh workflow run prepare-release.yml \
  --ref main \
  -f version=X.Y.Z \
  -f base_sha="$base_sha"
```

After the workflow finishes, open a PR from `release/vX.Y.Z` to `main`, review
the generated `CHANGELOG.md` entry, and merge it. Merging that release PR
triggers `publish-release.yml`, which creates the tag and GitHub release.

Use the next patch version unless the changes require a minor or major bump.
For example, if the latest tag is `v0.4.3`, the next patch release is `0.4.4`.

## Repository protection

The `main` branch is protected and requires the GitHub Actions status check
named `lint`. That check comes from the `lint` job in `.github/workflows/lint.yml`.
If the workflow or job name changes, update branch protection at the same time.

## Config overrides

| Linter | Rule | Default | Here | Reason |
|---|---|---|---|---|
| yamllint | `line-length` | enabled (max 80) | disabled | Traefik labels in docker-compose files routinely exceed 80 chars |
| pymarkdown | MD013 line-length | enabled | disabled | Tables and inline code in README files break when wrapped |
| pymarkdown | MD026 trailing-punctuation | enabled | disabled | `Setup:`, `Usage:` headings by convention |
| pymarkdown | MD034 no-bare-urls | enabled | disabled | Internal URLs referenced inline without link syntax |
| pymarkdown | MD024 no-duplicate-heading | strict | `allow_different_nesting: true` | Repeated subheadings under each section |
| ruff | E501 line-length | enabled (max 88) | disabled | Long error messages and inline expressions |
| shellcheck | SC1090/SC1091 | enabled | disabled | Dynamic `source` of `lib.sh` and `.env` |
| shellcheck | SC2029 | enabled | disabled | Variables in SSH commands expand client-side intentionally |
| shellcheck | SC2088 | enabled | disabled | Tilde in remote paths passed as-is to remote shell |
| shellcheck | SC2153/SC2154 | enabled | disabled | Variables set by `parse_apps` in `lib.sh` not visible to shellcheck |
| shellcheck | SC2001 | enabled | disabled | `sed` preferred over bash parameter expansion for regex substitution |

## Pre-commit hooks

Copy `.pre-commit-config.yaml.example` to your repo or add to your existing config:

```yaml
repos:
  - repo: git@github.com:rubykatzen/baseline.git
    rev: VERSION
    hooks:
      - id: yamllint
      - id: pymarkdown
      - id: ruff
      - id: shellcheck
      - id: actionlint
      - id: rubocop
      - id: erb-lint
```

Install the tools before running hooks:

```bash
python -m pip install yamllint pymarkdownlnt ruff
brew install shellcheck actionlint
```

Ruby GitHub Actions install Ruby automatically. If a `Gemfile` is present,
`setup-ruby` runs `bundle install` and linter actions use `bundle exec` —
so rubocop and erb_lint must be in the project `Gemfile`. If no `Gemfile`
is present, linter actions install required gems directly.

Add these gems to the caller repo `Gemfile` before enabling Ruby hooks
(both pre-commit and GitHub Actions):

```ruby
group :development, :test do
  gem "rubocop", require: false
  gem "standard", require: false
  gem "standard-custom", require: false
  gem "standard-performance", require: false
  gem "standard-rails", require: false
  gem "erb_lint", require: false
end
```

The `rubocop` pre-commit hook passes `--force-exclusion` so explicitly passed
filenames still respect RuboCop exclusions. The `erb-lint` pre-commit hook
matches HTML ERB templates only, mirroring `erb_lint --lint-all`.
