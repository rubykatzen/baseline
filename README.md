# dupmachine/linters

Shared linter configs and reusable workflows for all dupmachine repositories.

## Linters

| Linter | Files | Config |
|--------|-------|--------|
| [yamllint](https://github.com/adrienverge/yamllint) | `*.yml`, `*.yaml` | `configs/yamllint.yml` |
| [pymarkdown](https://github.com/jackdewinter/pymarkdown) | `*.md` | `configs/pymarkdown.json` |

## Deviations from defaults

### yamllint

| Rule | Default | Here |
|------|---------|------|
| `line-length` | enabled (max 80) | disabled |

### pymarkdown

| Rule | Default | Here |
|------|---------|------|
| MD013 line-length | enabled | disabled |
| MD026 trailing-punctuation | enabled | disabled — headings like `Setup:` are used intentionally |
| MD034 no-bare-urls | enabled | disabled — bare URLs appear intentionally in agent instruction files |
| MD024 no-duplicate-heading | enabled (strict) | `allow_different_nesting: true` — duplicate headings allowed under different parent headings |

## Usage

### Pre-commit

Copy `.pre-commit-config.yaml.example` to your repo as `.pre-commit-config.yaml`, or add the hooks to your existing config:

```yaml
repos:
  - repo: https://github.com/dupmachine/linters
    rev: main
    hooks:
      - id: yamllint
      - id: pymarkdown
```

Both linters must be installed on the system (`pip install yamllint pymarkdownlnt`).

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
    uses: dupmachine/linters/.github/workflows/yamllint.yml@main
  pymarkdown:
    uses: dupmachine/linters/.github/workflows/pymarkdown.yml@main
```

## Adding a new linter

See `AGENTS.md`.
