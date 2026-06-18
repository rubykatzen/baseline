# Baseline

Shared linter configs and composite GitHub Actions.

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

Non-Ruby actions install their own tools. Ruby linter actions require
`setup-ruby` first plus the `rubykatzen-baseline` gem and generated project
stubs described below.

### 2. Dependabot

Add `.github/dependabot.yml` to keep GitHub Actions and pre-commit pins
current automatically:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: daily
      time: "22:00"
      timezone: "Europe/Berlin"
  - package-ecosystem: pre-commit
    directory: /
    schedule:
      interval: daily
      time: "22:00"
      timezone: "Europe/Berlin"
```

Dependabot opens pull requests for version bumps. Pair with
`dependabot-automerge` if you want patch/minor updates merged automatically.

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

The `rubocop` and `erb-lint` pre-commit hooks and GitHub Actions require the
baseline gem in the project `Gemfile` plus the generated stubs above. They
delegate to the same `bundle exec` commands so local and CI linting use one
Bundler-resolved toolchain.

### Git source before RubyGems

```ruby
gem "rubykatzen-baseline", git: "git@github.com:rubykatzen/baseline.git", tag: "v0.5.0", require: false
```

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
| pymarkdown | MD041 first-line-h1 | enabled | disabled | Markdown fragments are often embedded under an existing document heading |
| pymarkdown | linter-pragmas extension | enabled | disabled | Inline linter suppressions must not bypass shared Markdown policy |
| pymarkdown | MD024 no-duplicate-heading | strict | `allow_different_nesting: true` | Repeated subheadings under each section |
| ruff | E501 line-length | enabled (max 88) | disabled | Long error messages and inline expressions |
| erb_lint/RuboCop | `Style/FrozenStringLiteralComment` | enabled | disabled | ERB comments do not act as Ruby magic comments in generated template code |
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
so `rubocop` and `erb_lint` must be available through the
[`rubykatzen-baseline`](#ruby-gem-rubocop--erb_lint) gem. Ruby hooks fail fast
when `Gemfile`, `.rubocop.yml`, or `.erb_lint.yml` stubs are missing.

The `rubocop` pre-commit hook passes `--force-exclusion` so explicitly passed
filenames still respect RuboCop exclusions. The `erb-lint` pre-commit hook
matches HTML ERB templates only, mirroring `erb_lint --lint-all`.
Hooks skip successfully when no matching project files are present.
