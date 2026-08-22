# Baseline

Baseline gives developers who move between language stacks a zero-configuration,
homogeneous development experience across repositories and organizations.

Connect the workflows a repository needs. Baseline detects applicable linters,
supplies their CI runtimes and configurations, and verifies shared policies and
files. Repositories satisfy those policies or declare explicit exceptions.

The examples use the latest
[Baseline release](https://github.com/rubykatzen/baseline/releases) and are
updated automatically with every release. Dependabot keeps the pin current in
consumer repositories.

## Lint automatically

Create `.github/workflows/lint.yml`:

<!-- x-release-please-start-version -->

```yaml
name: Lint
on:
  push:
    branches: ["main"]
  pull_request:
jobs:
  lint:
    uses: rubykatzen/baseline/.github/workflows/lint-shared.yml@v0.14.0
```

<!-- x-release-please-end -->

That is enough to get CI linting. Baseline inspects the tracked files, selects
every applicable linter, installs its runtime, and runs it with the canonical
configuration. Adding a new supported file type automatically enables its
linter on the next run.

When the repository contains `.pre-commit-config.yaml`, Baseline also checks
that its local hooks match the automatically selected CI linters.

## Check GitHub configuration

Create `.github/workflows/github.yml`:

<!-- x-release-please-start-version -->

```yaml
name: GitHub
on:
  push:
    branches: ["main"]
  pull_request:
jobs:
  github:
    uses: rubykatzen/baseline/.github/workflows/github-shared.yml@v0.14.0
```

<!-- x-release-please-end -->

Baseline checks the repository settings and labels against
[`config/github.yml`](config/github.yml). This includes squash-only merging,
automatic branch deletion, auto-merge, and the canonical label set and colors.
Release Please labels are allowed but optional.

## Check shared repository files

Create `.github/workflows/embedder.yml`:

<!-- x-release-please-start-version -->

```yaml
name: Embedder
on:
  push:
    branches: ["main"]
  pull_request:
jobs:
  embedder:
    uses: rubykatzen/baseline/.github/workflows/embedder-shared.yml@v0.14.0
```

<!-- x-release-please-end -->

Baseline checks that the repository contains every fragment declared in
[`config/embedder.yml`](config/embedder.yml), including the shared Dependabot
configuration and agent instructions. A failure reports all differences, not
only the first missing fragment.

Repositories using an optional shared policy can add its Embedder configuration:

<!-- x-release-please-start-version -->

```yaml
jobs:
  embedder:
    uses: rubykatzen/baseline/.github/workflows/embedder-shared.yml@v0.14.0
    with:
      extra: '["release-please"]'
```

<!-- x-release-please-end -->

Optional configurations live under [`config/embedder/`](config/embedder/). The
`release-please` configuration checks the common release configuration, workflow,
and pull request title policy while leaving package-specific publishing local.

## Notify Telegram about pull requests

Create `.github/workflows/notify-telegram-pr.yml`:

<!-- x-release-please-start-version -->

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
    uses: rubykatzen/baseline/.github/workflows/notify-telegram-pr-shared.yml@v0.14.0
    secrets:
      TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
      TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```

<!-- x-release-please-end -->

Baseline sends notifications for opened, reopened, ready, and merged pull
requests, plus a daily digest of up to ten open non-draft pull requests. Empty
digests do not send a message.

`pull_request_target` keeps Telegram secrets available while loading trusted
workflow code from the default branch. The shared workflow does not check out
or execute pull request code. Pass the two secrets explicitly rather than using
`secrets: inherit`.

## Notify Telegram about closed issues

Issue notifications are optional and can use a different Telegram channel from
pull request notifications. Create `.github/workflows/notify-telegram-issue.yml`:

<!-- x-release-please-start-version -->

```yaml
name: Notify Telegram issue
on:
  issues:
    types: [closed]
jobs:
  notify:
    if: contains(github.event.issue.labels.*.name, 'notify')
    uses: rubykatzen/baseline/.github/workflows/notify-telegram-issue-shared.yml@v0.14.0
    secrets:
      TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
      TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_ISSUE_CHAT_ID }}
```

<!-- x-release-please-end -->

The caller decides which closed issues should produce a notification. Change or
remove the `if` condition to match the repository's policy. Baseline only
formats and sends the message; it does not modify the issue or its labels.

## Explicit exceptions

Automatic policy is the default. When a repository intentionally differs, pass
a JSON array through `skip`:

<!-- x-release-please-start-version -->

```yaml
jobs:
  lint:
    uses: rubykatzen/baseline/.github/workflows/lint-shared.yml@v0.14.0
    with:
      skip: '["rubocop", "herb"]'
```

<!-- x-release-please-end -->

The GitHub and Embedder workflows use the same convention:

```yaml
with:
  skip: '["labels"]'
```

```yaml
with:
  skip: '["message-prefix"]'
```

Fragments from an optional Embedder configuration use the
`<configuration>/<fragment>` namespace and can be skipped independently:

```yaml
with:
  extra: '["release-please"]'
  skip: '["release-please/include-component-in-tag"]'
```

Omit `release-please` from `extra` instead when none of its policy should apply.
Unknown names fail the workflow. A skipped linter must also be absent from the
Baseline entry in `.pre-commit-config.yaml`, keeping local and CI linting equal.

## Local linting

CI runtime installation is automatic. For local pre-commit use, create
`.pre-commit-config.yaml` and keep only the hooks relevant to the repository:

<!-- x-release-please-start-version -->

```yaml
repos:
  - repo: https://github.com/rubykatzen/baseline
    rev: v0.14.0
    hooks:
      - id: yamllint
      - id: pymarkdown
      - id: ruff
      - id: tombi
      - id: shellcheck
      - id: actionlint
      - id: rubocop
      - id: erb-lint
      - id: herb
```

<!-- x-release-please-end -->

Pre-commit hooks are thin wrappers and expect their tools on `PATH`. Install the
Python and standalone tools used by the repository:

```bash
python -m pip install pre-commit yamllint pymarkdownlnt ruff tombi
brew install shellcheck actionlint
```

### Ruby projects

Ruby projects get RuboCop, erb_lint, and Herb, with Baseline's configuration,
from one gem:

```ruby
group :development, :test do
  gem "rubykatzen-baseline", require: false
end
```

After `bundle install`, create the project config stubs:

```bash
bundle exec baseline-install
```

The generated `.rubocop.yml` and `.erb_lint.yml` inherit the configs shipped in
the gem. Project-specific existing violations can remain in
`.rubocop_todo.yml` or `.erb_lint_todo.yml`; Baseline continues to catch new
violations.

## Keep Baseline current

Dependabot keeps workflow references, pre-commit hooks, Python packages, and
Ruby gems current. The Embedder workflow verifies the canonical
`.github/dependabot.yml`, so consumer repositories do not maintain that
configuration independently.

Dependabot opens `chore(deps):` pull requests, which do not request a release by
default. Rename a release-worthy dependency update to `fix(deps):` to request a
patch release.

## Supported linters

| Key | Files | Configuration |
|---|---|---|
| `yamllint` | `*.yml`, `*.yaml` | `config/yamllint.yml` |
| `pymarkdown` | Markdown | `config/pymarkdown.json` |
| `ruff` | Python source and stubs | `config/ruff.toml` |
| `tombi` | `*.toml` | consumer config or Tombi defaults |
| `shellcheck` | `*.sh` | `config/shellcheck.rc` |
| `actionlint` | GitHub Actions workflows | actionlint defaults |
| `rubocop` | Ruby source, Gemfiles, Rakefiles, and gemspecs | `config/rubocop.yml` |
| `erb-lint` | HTML ERB templates | `config/erb_lint.yml` |
| `herb` | HTML and Rails template variants | Herb defaults |

See [LINTERS-DEFAULTS-OVERRIDES.md](LINTERS-DEFAULTS-OVERRIDES.md) for deliberate
deviations from upstream linter defaults.

## License

Baseline is released under the [MIT License](LICENSE).
