#!/bin/sh

has_actionlint_targets() {
  [ -d .github/workflows ] || return 1

  find .github/workflows \
    -type f \
    \( -name '*.yml' -o -name '*.yaml' \) \
    -print -quit | grep -q .
}

if ! has_actionlint_targets; then
  printf '%s\n' 'No GitHub Actions workflow files found; skipping actionlint.'
  exit 0
fi

exec actionlint "$@"
