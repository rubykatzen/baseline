# dupmachine/workflows

Shared linter configs and reusable workflows for all dupmachine repositories.

## Linters

| Linter | Files | Config |
|--------|-------|--------|
| [yamllint](https://github.com/adrienverge/yamllint) | `*.yml`, `*.yaml` | `configs/yamllint.yml` |
| [pymarkdown](https://github.com/jackdewinter/pymarkdown) | `*.md` | `configs/pymarkdown.json` |
| [ruff](https://github.com/astral-sh/ruff) | `*.py` | `configs/ruff.toml` |
| [shellcheck](https://github.com/koalaman/shellcheck) | `*.sh` | `configs/shellcheck.rc` |
| [actionlint](https://github.com/rhysd/actionlint) | `.github/workflows/*.yml` | — |

## Overrides

| Linter | Rule | Default | Here | Reason |
|--------|------|---------|------|--------|
| yamllint | `line-length` | enabled (max 80) | disabled | Traefik labels in docker-compose files (e.g. `traefik.http.routers.${APP_NAME}.tls.certresolver=...`) routinely exceed 80 chars and cannot be meaningfully wrapped |
| pymarkdown | MD013 line-length | enabled | disabled | Tables and inline code references in README files break when wrapped |
| pymarkdown | MD026 trailing-punctuation | enabled | disabled | AGENTS.md files use `Setup:`, `Usage:`, `Configuration:` as section headings by convention |
| pymarkdown | MD034 no-bare-urls | enabled | disabled | AGENTS.md files reference internal URLs (e.g. Semaphore) inline without link syntax |
| pymarkdown | MD024 no-duplicate-heading | enabled (strict) | `allow_different_nesting: true` | Playbook docs repeat identical subheadings (e.g. `### Usage example`) under each playbook section |
| ruff | E501 line-length | enabled (max 88) | disabled | Long error messages and inline expressions in Python scripts exceed 88 chars and cannot be meaningfully wrapped |
| shellcheck | SC1090/SC1091 | enabled | disabled | Dynamic `source` of `lib.sh` and `.env` — shellcheck can't follow them but they are always present at runtime |
| shellcheck | SC2029 | enabled | disabled | Variables in SSH commands intentionally expand on the client side before being passed to the remote shell |
| shellcheck | SC2088 | enabled | disabled | Tilde in remote path strings is intentionally passed as-is to the remote shell via SSH, not expanded locally |
| shellcheck | SC2153/SC2154 | enabled | disabled | Variables set by `parse_apps` in `lib.sh` are not visible to shellcheck due to SC1091 |
| shellcheck | SC2001 | enabled | disabled | Style preference: `sed` is clearer than bash parameter expansion for regex substitution |

## Usage

### Pre-commit

Copy `.pre-commit-config.yaml.example` to your repo as `.pre-commit-config.yaml`, or add the hooks to your existing config:

```yaml
repos:
  - repo: https://github.com/dupmachine/workflows
    rev: main
    hooks:
      - id: yamllint
      - id: pymarkdown
      - id: ruff
      - id: shellcheck
      - id: actionlint
```

Required system dependencies: `pip install yamllint pymarkdownlnt ruff`, `brew install shellcheck actionlint`.

### GitHub Actions

Add jobs to your `lint.yml` workflow:

```yaml
name: Lint
on:
  push:
    branches: ["main"]
  pull_request:
jobs:
  yamllint:
    uses: dupmachine/workflows/.github/workflows/yamllint.yml@main
  pymarkdown:
    uses: dupmachine/workflows/.github/workflows/pymarkdown.yml@main
  ruff:
    uses: dupmachine/workflows/.github/workflows/ruff.yml@main
  shellcheck:
    uses: dupmachine/workflows/.github/workflows/shellcheck.yml@main
  actionlint:
    uses: dupmachine/workflows/.github/workflows/actionlint.yml@main
```

## Adding a new linter

See `AGENTS.md`.
