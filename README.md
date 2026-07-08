# Baseline

Shared linter configs and thin wrappers.

Baseline is responsible for canonical configuration only. Consuming
repositories are responsible for installing runtimes and linter binaries before
running baseline hooks or actions.

## Quick setup

Replace `VERSION` in all examples with the latest release tag from
[github.com/rubykatzen/baseline/releases](https://github.com/rubykatzen/baseline/releases).
After initial setup, [Dependabot](#3-dependabot) keeps the pin current automatically.

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
    uses: rubykatzen/baseline/.github/workflows/lint-shared.yml@VERSION
    with:
      linters: yamllint, pymarkdown, ruff, shellcheck, actionlint, rubocop, erb-lint, herb, pre-commit
```

`lint-shared.yml` installs runtimes and runs each linter automatically. Add
`pre-commit` to `linters` to enforce that `.pre-commit-config.yaml` hooks stay
in sync with CI.

### 2. Pre-commit hooks

Copy `.pre-commit-config.yaml.example` to your repo or add to your existing config.
Include only the hooks relevant to your stack:

```yaml
repos:
  - repo: https://github.com/rubykatzen/baseline
    rev: v0.7.8
    hooks:
      - id: yamllint
      - id: pymarkdown
      - id: ruff
      - id: shellcheck
      - id: actionlint
      - id: rubocop
      - id: erb-lint
```

Remove hooks you don't need. Install the tools before running hooks:

```bash
python -m pip install yamllint pymarkdownlnt ruff
brew install shellcheck actionlint
```

Ruby hooks use `bundle exec`; install Ruby and run `bundle install` in the
consuming repository first. `rubocop` and `erb_lint` must be available through
the [`rubykatzen-baseline`](#ruby-gem-rubocop--erb_lint) gem.

### 3. Dependabot

Add `.github/dependabot.yml` to keep GitHub Actions and pre-commit pins
current automatically:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: daily
      time: "10:00"
      timezone: "Europe/Berlin"
  - package-ecosystem: pre-commit
    directory: /
    schedule:
      interval: daily
      time: "10:00"
      timezone: "Europe/Berlin"
```

Dependabot opens pull requests for version bumps. Pair with
`dependabot-automerge` if you want patch/minor updates merged automatically.

---

## Composite actions (linters)

Pass these keys to `lint-shared.yml` via `linters:`:

| Key | Action | Lints | Config |
|---|---|---|---|
| `yamllint` | `lint-yamllint` | `*.yml`, `*.yaml` | `config/yamllint.yml` |
| `pymarkdown` | `lint-pymarkdown` | `*.md` | `config/pymarkdown.json` |
| `ruff` | `lint-ruff` | `*.py` | `config/ruff.toml` |
| `shellcheck` | `lint-shellcheck` | `*.sh` | `config/shellcheck.rc` |
| `actionlint` | `lint-actionlint` | `.github/workflows/*.yml` | — |
| `rubocop` | `lint-rubocop` | `*.rb` | `config/rubocop.yml` |
| `erb-lint` | `lint-erb-lint` | `*.erb` | `config/erb_lint.yml` |
| `herb` | `lint-herb` | `*.html.erb`, `*.html+*.erb`, `*.turbo_stream.erb`, `*.herb`, `*.rhtml` | — |
| `pre-commit` | `check-precommit-sync` | `.pre-commit-config.yaml` | — |

`check-precommit-sync` runs two checks:

1. **Coverage** — scans repo files and verifies that every baseline hook whose file type is present is configured in `.pre-commit-config.yaml`
2. **Sync** — verifies that configured hooks match the `linters` input (minus `pre-commit` itself)

## Ruby gem (RuboCop + erb_lint)

For Rails and other Ruby projects, install the shared configs through the `rubykatzen-baseline`
gem instead of listing RuboCop gems separately. Configs still live in this
repository and ship inside the gem — consumer repos only add stub files that
inherit from the gem.

### 1. Gemfile

Replace individual RuboCop gems with a single baseline pin:

```ruby
group :development, :test do
  gem "rubykatzen-baseline", require: false
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

## Linters: defaults & overrides

See [LINTERS-DEFAULTS-OVERRIDES.md](LINTERS-DEFAULTS-OVERRIDES.md) for a full list of deviations from each linter's defaults with rationale.
