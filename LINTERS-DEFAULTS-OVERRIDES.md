# Config overrides

Deviations from each linter's defaults. Rules are disabled only when impractical
across all repos, not to accommodate a single project.

## yamllint

| Rule | Default | Here | Reason |
|---|---|---|---|
| `line-length` | enabled (max 80) | disabled | Traefik labels in docker-compose files routinely exceed 80 chars |
| `document-start` | `present: false` | disabled | Ruby's Psych always emits `---`; cannot be suppressed via options |
| `indentation.indent-sequences` | `true` | `consistent` | Psych outputs sequences at the parent key level; `consistent` allows either style as long as each file is uniform |

## pymarkdown

| Rule | Default | Here | Reason |
|---|---|---|---|
| MD013 line-length | enabled | disabled | Tables and inline code in README files break when wrapped |
| MD022 blanks-around-headings | enabled | disabled | HTML comments placed directly above headings trigger false positives |
| MD026 trailing-punctuation | enabled | disabled | `Setup:`, `Usage:` headings by convention |
| MD034 no-bare-urls | enabled | disabled | Internal URLs referenced inline without link syntax |
| MD041 first-line-h1 | enabled | disabled | Markdown fragments are often embedded under an existing document heading |
| linter-pragmas extension | enabled | disabled | Inline linter suppressions must not bypass shared Markdown policy |
| MD024 no-duplicate-heading | strict | `allow_different_nesting: true` | Repeated subheadings under each section |

## ruff

| Rule | Default | Here | Reason |
|---|---|---|---|
| line-length | 88 | 160 | Aligns with RuboCop; long error messages and inline expressions |

## RuboCop

| Rule | Default | Here | Reason |
|---|---|---|---|
| `Layout/LineLength` | disabled | max 160 | Aligns with Ruff; long lines are an error, not just style |
| `Style/TrailingCommaInArguments` | `no_comma` | `comma` | Aligns with Ruff/Black magic trailing comma: forces multiline to stay multiline, cleaner diffs |
| `Style/TrailingCommaInArrayLiteral` | `no_comma` | `comma` | Same as above |
| `Style/TrailingCommaInHashLiteral` | `no_comma` | `comma` | Same as above |
| `Bundler/OrderedGems` | disabled | enabled | Aligns with Ruff isort: consistent ordering reduces merge conflicts |
| `Gemspec/OrderedDependencies` | disabled | enabled | Same as above |
| `Style/RequireOrder` | disabled | enabled | Aligns with Ruff isort: alphabetical `require` ordering |
| `Style/StringConcatenation` | disabled | enabled | Aligns with Ruff UP032: prefer interpolation over `+` concatenation |
| `Style/SafeNavigation` | `ConvertCodeThatCanStartToReturnNil: false` | `true` | Ruby-native alternative to collapsing nested nil-guard ifs |
| `Style/DisableCopsWithinSourceCodeDirective` | disabled | enabled | Inline `# rubocop:disable` comments must not bypass shared policy |
| `Style/FrozenStringLiteralComment` | disabled | enabled | All Ruby files must declare frozen string literal |
| `Rails/ActionOrder` | disabled | enabled | Enforces canonical controller action ordering |
| `Rails/HasManyOrHasOneDependent` | disabled | enabled | Associations must declare `dependent:` to prevent orphaned records |
| `Rails/InverseOf` | disabled | enabled | Associations must declare `inverse_of:` for bidirectional awareness |
| `Rails/ActionFilter` | disabled | enabled | Prefer `before_action` over deprecated `before_filter` |
| `Rails/NegateInclude` | disabled | enabled | Prefer `exclude?` over `!include?` |
| `Rails/Present` | disabled | enabled | Prefer `present?` over `!blank?` |
| `Rails/RedundantActiveRecordAllMethod` | disabled | enabled | Prefer `Model.where(...)` over `Model.all.where(...)` |

## erb_lint / RuboCop in ERB

| Rule | Default | Here | Reason |
|---|---|---|---|
| `Style/FrozenStringLiteralComment` | enabled | disabled | ERB comments do not act as Ruby magic comments in generated template code |

## shellcheck

| Rule | Default | Here | Reason |
|---|---|---|---|
| SC1090/SC1091 | enabled | disabled | Dynamic `source` of `lib.sh` and `.env` |
| SC2029 | enabled | disabled | Variables in SSH commands expand client-side intentionally |
| SC2088 | enabled | disabled | Tilde in remote paths passed as-is to remote shell |
| SC2153/SC2154 | enabled | disabled | Variables set by `parse_apps` in `lib.sh` not visible to shellcheck |
| SC2001 | enabled | disabled | `sed` preferred over bash parameter expansion for regex substitution |
