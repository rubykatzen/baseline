#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
bundle exec rubocop --config "$BASELINE_DIR/configs/rubocop.yml" "$@"
