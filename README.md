# Baseline

Shared linter configs and thin wrappers.

Baseline owns canonical configuration and runtime installation in CI. Consuming
repositories install runtimes and linter binaries only for local pre-commit use.

## Quick setup

Replace `VERSION` in all examples with the latest release tag from
[github.com/rubykatzen/baseline/releases](https://github.com/rubykatzen/baseline/releases).
After initial setup, [Dependabot](#7-dependabot) keeps the pin current automatically.

### 1. Lint workflow

Create `.github/workflows/lint.yml`:

```yaml
name: Lint
on:
  push:
    branches: ["main"]
  pull_request:
jobs:
  lint:
    uses: rubykatzen/baseline/.github/workflows/lint-shared.yml@VERSION
```

`lint-shared.yml` inspects tracked files, selects every applicable baseline
linter, installs its runtime, and runs it automatically. A tracked
`.pre-commit-config.yaml` also enables the pre-commit sync check.

Skip linters explicitly when a repository does not want an otherwise
applicable check:

```yaml
jobs:
  lint:
    uses: rubykatzen/baseline/.github/workflows/lint-shared.yml@VERSION
    with:
      skip: '["rubocop", "herb"]'
```

Skipped linters must also be removed from the baseline entry in
`.pre-commit-config.yaml` so local and CI linting remain identical. Unknown
skip names fail the workflow.

### 2. GitHub repository config

Create `.github/workflows/github.yml`:

```yaml
name: GitHub
on:
  push:
    branches: ["main"]
  pull_request:
jobs:
  github-config-check:
    uses: rubykatzen/baseline/.github/workflows/github-shared.yml@VERSION
```

The shared workflow checks repository settings against `config/github.yml`.
The policy requires the wiki to be disabled, auto-merge to be enabled, merged
branches to be deleted automatically, and pull requests to use squash-only
merging with the pull request title as the complete resulting commit message.

Skip checks explicitly when a repository needs an exception:

```yaml
jobs:
  github-config-check:
    uses: rubykatzen/baseline/.github/workflows/github-shared.yml@VERSION
    with:
      skip: '["hasWikiEnabled"]'
```

The `skip` input must be a JSON array. Unknown check names fail the workflow.

### 3. Telegram pull request notifications

Create `.github/workflows/notify-telegram-pr.yml`:

```yaml
name: Notify Telegram PR
on:
  pull_request_target:
    types: [opened, ready_for_review, reopened, closed]
  schedule:
    - cron: "0 10 * * *"
  workflow_dispatch:
jobs:
  notify:
    uses: rubykatzen/baseline/.github/workflows/notify-telegram-pr-shared.yml@VERSION
    secrets:
      TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
      TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```

The workflow reports non-draft pull requests when they are opened, reopened,
or marked ready for review, reports merged pull requests, and sends a daily
digest of open non-draft pull requests. An empty digest sends no message.

`pull_request_target` loads trusted workflow code from the default branch so
Telegram secrets remain available without executing or checking out pull
request code. Pass the two secrets explicitly; do not use `secrets: inherit`.

### 4. Telegram issue notifications

Issue notifications are optional. A repository that needs them creates
`.github/workflows/notify-telegram-issue.yml`:

```yaml
name: Notify Telegram issue
on:
  issues:
    types: [closed]
jobs:
  notify:
    if: contains(github.event.issue.labels.*.name, 'notify')
    uses: rubykatzen/baseline/.github/workflows/notify-telegram-issue-shared.yml@VERSION
    secrets:
      TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
      TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_ISSUE_CHAT_ID }}
```

This example reports only issues carrying the `notify` label at close time.
The caller owns this condition and may replace it or omit it to report every
closed issue. The shared workflow only formats and sends the notification; it
does not modify the issue. The message includes up to 500 characters of the
issue body. PR and issue callers may map `TELEGRAM_CHAT_ID` to different
repository secrets and therefore different channels.

### 5. Embedded content

Create `.github/workflows/embedder.yml`:

```yaml
name: Embedder
on:
  push:
    branches: ["main"]
  pull_request:
jobs:
  embedded-content-check:
    uses: rubykatzen/baseline/.github/workflows/embedder-shared.yml@VERSION
```

The shared workflow checks repository files against the required fragments in
`config/embedder.yml`. Each named fragment has a target path and content that
must occur in that file. Multiple fragments may target the same file. Ownership
markers are part of the configured content, so the checker remains independent
of the target file format. Failures report every fragment and file, followed by
a unified diff for each missing or outdated fragment.

Skip fragments explicitly when a repository needs an exception:

```yaml
jobs:
  embedded-content-check:
    uses: rubykatzen/baseline/.github/workflows/embedder-shared.yml@VERSION
    with:
      skip: '["message-prefix"]'
```

The `skip` input must be a JSON array. Unknown fragment names fail the workflow.

### 6. Pre-commit hooks

Copy `.pre-commit-config.yaml.example` to your repo or add to your existing config.
Include only the hooks relevant to your stack:

```yaml
repos:
  - repo: https://github.com/rubykatzen/baseline
    rev: v0.9.0 # x-release-please-version
    hooks:
      - id: yamllint
      - id: pymarkdown
      - id: ruff
      - id: tombi
      - id: shellcheck
      - id: actionlint
      - id: rubocop
      - id: erb-lint
```

Remove hooks that are skipped by the shared workflow or have no matching
tracked files. Install the tools before running hooks:

```bash
python -m pip install yamllint pymarkdownlnt ruff tombi
brew install shellcheck actionlint
```

Ruby hooks use `bundle exec`; install Ruby and run `bundle install` in the
consuming repository first. `rubocop` and `erb_lint` must be available through
the [`rubykatzen-baseline`](#ruby-gem-rubocop--erb_lint) gem.

### 7. Dependabot

Add `.github/dependabot.yml` to keep GitHub Actions and pre-commit pins
current automatically:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    labels: []
    commit-message:
      prefix: chore
      include: scope
    schedule:
      interval: daily
      time: "10:00"
      timezone: "Europe/Berlin"
  - package-ecosystem: pre-commit
    directory: /
    labels: []
    commit-message:
      prefix: chore
      include: scope
    schedule:
      interval: daily
      time: "10:00"
      timezone: "Europe/Berlin"
```

The commit message configuration also prefixes pull request titles with
`chore(deps):`, so they pass the commit workflow without creating a release by
default. Rename a release-worthy dependency update to `fix(deps):` to request a
patch release. Pair Dependabot with
`dependabot-automerge` if you want patch/minor updates merged automatically.

---

## Automatic linter selection

The shared workflow can select these keys. Put a key in `skip` to
disable it for a repository:

| Key | Action | Lints | Config |
|---|---|---|---|
| `yamllint` | `lint-yamllint` | `*.yml`, `*.yaml` | `config/yamllint.yml` |
| `pymarkdown` | `lint-pymarkdown` | `*.md` | `config/pymarkdown.json` |
| `ruff` | `lint-ruff` | `*.py` | `config/ruff.toml` |
| `tombi` | `lint-tombi` | `*.toml` | consumer config or Tombi defaults |
| `shellcheck` | `lint-shellcheck` | `*.sh` | `config/shellcheck.rc` |
| `actionlint` | `lint-actionlint` | `.github/workflows/*.yml` | — |
| `rubocop` | `lint-rubocop` | `*.rb` | `config/rubocop.yml` |
| `erb-lint` | `lint-erb-lint` | `*.erb` | `config/erb_lint.yml` |
| `herb` | `lint-herb` | `*.html.erb`, `*.html+*.erb`, `*.turbo_stream.erb`, `*.herb`, `*.rhtml` | — |
| `pre-commit` | `check-precommit` | `.pre-commit-config.yaml` | — |

The detector scans `git ls-files` and matches each file against the `types` or
`files` selector in `.pre-commit-hooks.yaml`. It adds `pre-commit` when a
`.pre-commit-config.yaml` is present, then removes the linters listed in `skip`.

Tombi discovers a consumer repository's `tombi.toml`, `.tombi.toml`, or
`[tool.tombi]` configuration. Without one, Tombi's defaults apply. Baseline runs
both linting and formatting checks offline and treats lint warnings as errors.

`check-precommit` verifies that configured baseline hooks exactly match
the detected CI linters, minus `pre-commit` itself.

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

Release Please maintains a release pull request from Conventional Commits on
`main`. Review its proposed version, changelog, and file updates, then merge the
pull request to release. The merge creates the version tag and GitHub Release,
publishes `rubykatzen-baseline` to RubyGems, and updates the floating major and
minor tags used by consumers.

The release workflow uses the `RELEASE_TOKEN` repository secret so its
pull requests trigger required CI. Use a fine-grained personal access token
limited to this repository with read and write access to contents, issues, and
pull requests.

## Linters: defaults & overrides

See [LINTERS-DEFAULTS-OVERRIDES.md](LINTERS-DEFAULTS-OVERRIDES.md) for a full list of deviations from each linter's defaults with rationale.
