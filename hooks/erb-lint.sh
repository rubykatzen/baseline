#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
bundle exec erb_lint --config "$BASELINE_DIR/configs/erb-lint.yml" "$@"
