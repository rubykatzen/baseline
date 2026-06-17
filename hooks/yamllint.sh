#!/bin/sh

has_yamllint_targets() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.yml' -o -name '*.yaml' \) \
    -print -quit | grep -q .
}

if ! has_yamllint_targets; then
  printf '%s\n' 'No YAML files found; skipping yamllint.'
  exit 0
fi

exec yamllint -c "$(dirname "$0")/../config/yamllint.yml" "$@"
