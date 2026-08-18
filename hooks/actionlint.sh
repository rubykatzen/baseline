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

# Remove these ignores once actionlint supports GitHub's reusable workflow additions:
# https://github.com/rhysd/actionlint/issues/705
# https://github.com/rhysd/actionlint/issues/711
exec actionlint \
  -ignore 'property "workflow_(repository|sha)" is not defined in object type' \
  -ignore 'specifying action "\$/.+" in invalid format because ref is missing' \
  -ignore 'reusable workflow call "\$/.+" at "uses" is not following the format' \
  "$@"
