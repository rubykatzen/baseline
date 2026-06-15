#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cat > .rubocop.yml << RUBOCOP
inherit_from:
  - $BASELINE_DIR/configs/rubocop.yml
  - .rubocop_todo*.yml
RUBOCOP

trap "rm -f .rubocop.yml" EXIT
bundle exec rubocop "$@"
