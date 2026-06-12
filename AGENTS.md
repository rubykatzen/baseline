# AGENTS.md

This file provides guidance to AI coding agents when working with this repository.

## Purpose

This repo is the single source of truth for linter configs across all dupmachine repositories. The goal is identical linting everywhere — configs live here and nowhere else.

## Repository Structure

- `configs/` — canonical linter config files
- `hooks/` — shell script wrappers for pre-commit (`language: script`)
- `.github/actions/` — reusable composite GitHub Actions for linting and releases
- `.github/workflows/` — repository-owned workflows for baseline linting and releases
- `.pre-commit-hooks.yaml` — hook definitions for pre-commit
- `.pre-commit-config.yaml.example` — example for consuming repos

## Adding a New Linter

To add a linter for a new file type:

1. Add config to `configs/<linter>.ext`
2. Add `hooks/<linter>.sh` — shell wrapper that passes the config path via `$(dirname "$0")/../configs/<linter>.ext`
3. Make the script executable: `chmod +x hooks/<linter>.sh`
4. Add hook entry to `.pre-commit-hooks.yaml`
5. Add composite action to `.github/actions/lint-<linter>/action.yml`
6. Update `.pre-commit-config.yaml.example`
7. Update `README.md`

## Self-linting

Baseline lints itself through `.github/workflows/lint.yml` using local composite
actions (`./.github/actions/lint-*`). Do not point the baseline self-lint
workflow at `dupmachine/baseline@latest`; it must validate the actions and
configs from the current commit.

## Linter Selection

For language-agnostic file types (YAML, Markdown, shell, etc.), always choose the linter implemented in the highest-priority runtime:

**Python > TypeScript > everything else**

This avoids introducing new runtimes into repos that don't already use them.

## Disabled Rules

Rules are disabled only when impractical across all repos, not to accommodate a single repo. Per-repo overrides are not supported by design. Deviations from defaults are documented in `README.md`.
