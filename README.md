# Baseline

Shared linter configs, composite GitHub Actions, and reusable workflows.

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

### 3. Pre-commit autoupdate (optional)

Create `.github/workflows/pre-commit-autoupdate.yml`:

```yaml
name: Pre-commit Autoupdate
on:
  schedule:
    - cron: "30 21 * * *"  # 22:30 Europe/Berlin (UTC+1)
  workflow_dispatch:
jobs:
  autoupdate:
    uses: rubykatzen/baseline/.github/workflows/pre-commit-autoupdate-shared.yml@VERSION
    secrets: inherit
```

Runs `pre-commit autoupdate` daily and commits the result directly to `main`.

---

## Composite actions (linters)

| Action | Lints | Config |
|---|---|---|
| `lint-yamllint` | `*.yml`, `*.yaml` | `config/yamllint.yml` |
| `lint-pymarkdown` | `*.md` | `config/pymarkdown.json` |
| `lint-ruff` | `*.py` | `config/ruff.toml` |
| `lint-shellcheck` | `*.sh` | `config/shellcheck.rc` |
| `lint-actionlint` | `.github/workflows/*.yml` | — |
| `lint-rubocop` | `*.rb` | `config/rubocop.yml` |
| `lint-erb-lint` | `*.erb` | `config/erb_lint.yml` |
| `lint-herb` | `*.html.erb`, `*.herb`, `*.turbo_stream.erb` | — |

## Ruby gem (RuboCop + erb_lint)

For Rails and other Ruby projects, install the shared configs through the `rubykatzen-baseline`
gem instead of listing RuboCop gems separately. Configs still live in this
repository and ship inside the gem — consumer repos only add stub files that
inherit from the gem.

### 1. Gemfile

Replace individual RuboCop gems with a single baseline pin. Match the gem
version to the git tag (for example tag `v0.5.0` → gem `0.5.0`):

```ruby
group :development, :test do
  gem "rubykatzen-baseline", "0.5.0", require: false
end
```

The gem pulls in `rubocop`, `rubocop-performance`, `rubocop-rails`,
`standard-custom`, and `erb_lint` as dependencies.

### 2. Project stubs

Run once from the project root after `bundle install`:

```bash
bundle exec baseline-install
```

This creates stub configs when missing:

```yaml
# .rubocop.yml
inherit_gem:
  rubykatzen-baseline: config/rubocop.yml

# Generate project-specific excludes, then uncomment inherit_from below:
#   bundle exec rubocop --auto-gen-config --auto-gen-only-exclude --exclude-limit 10000
# inherit_from:
#   - .rubocop_todo.yml
```

```yaml
# .erb_lint.yml
inherit_gem:
  rubykatzen-baseline: config/erb_lint.yml

# Generate .erb_lint_todo.yml, then uncomment inherit_from below:
#   bundle exec erb_lint --enable-all-linters --lint-all
# inherit_from:
#   - .erb_lint_todo.yml
```

Stubs work out of the box with shared baseline cops only. Uncomment
`inherit_from` after creating todo files for project-specific excludes.

### 3. erb_lint todo file

erb_lint has no `--auto-gen-config`. To suppress existing violations while
keeping new ones visible, create `.erb_lint_todo.yml` manually:

1. Run erb_lint and collect the cop names that appear:

   ```bash
   bundle exec erb_lint --lint-all
   ```

2. Create `.erb_lint_todo.yml` in the project root. Use the erb_lint config
   format — cop names go inside `linters.Rubocop.rubocop_config`, not at the
   top level:

   ```yaml
   # .erb_lint_todo.yml
   # Remove cops from this list as you fix templates.
   linters:
     Rubocop:
       rubocop_config:
         Layout/ArgumentAlignment:
           Enabled: false
         Style/FrozenStringLiteralComment:
           Enabled: false
   ```

3. Uncomment `inherit_from` in `.erb_lint.yml`:

   ```yaml
   inherit_gem:
     rubykatzen-baseline: config/erb_lint.yml

   inherit_from:
     - .erb_lint_todo.yml
   ```

Remove cops from the todo file as you fix the templates.

### 4. Local commands

```bash
bundle exec rubocop
bundle exec rubocop -A
bundle exec erb_lint --lint-all
```

Pre-commit hooks and GitHub Actions detect these stubs and delegate to the same
commands when a `Gemfile` is present. Without stubs, hooks fall back to the
shell wrappers that assemble a temporary config from this repository checkout.

### Git source before RubyGems

```ruby
gem "rubykatzen-baseline", git: "git@github.com:rubykatzen/baseline.git", tag: "v0.5.0", require: false
```

## Reusable workflows

| Workflow | Trigger in caller | What it does |
|---|---|---|
| `pre-commit-autoupdate-shared.yml` | `schedule` / `workflow_dispatch` | Runs `pre-commit autoupdate` and commits to main |

## Releases

Baseline releases are cut with the
[rubykatzen/releaser](https://github.com/rubykatzen/releaser) CLI. Run from
inside this repository:

```bash
releaser patch   # or: releaser minor / releaser major
```

The CLI verifies that CI is green on `origin/main`, calculates the next version,
dispatches `prepare-release.yml`, watches it run, then opens a `release/vX.Y.Z`
PR and enables auto-merge. `publish-release.yml` fires automatically once the PR
merges and creates the tag and GitHub release.

Check release readiness without triggering anything:

```bash
releaser status
releaser patch --dry-run
```

Install the CLI:

```bash
brew tap rubykatzen/tap && brew install releaser
```

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
(both pre-commit and GitHub Actions) when not using the baseline gem:

```ruby
group :development, :test do
  gem "rubocop", require: false
  gem "rubocop-performance", require: false
  gem "rubocop-rails", require: false
  gem "standard-custom", require: false
  gem "erb_lint", require: false
end
```

Prefer the [baseline gem](#ruby-gem-rubocop--erb_lint) when the project already
uses Bundler.

The `rubocop` pre-commit hook passes `--force-exclusion` so explicitly passed
filenames still respect RuboCop exclusions. The `erb-lint` pre-commit hook
matches HTML ERB templates only, mirroring `erb_lint --lint-all`.
Hooks skip successfully when no matching project files are present.
