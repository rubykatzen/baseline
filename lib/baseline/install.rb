# frozen_string_literal: true

module Baseline
  class Install
    STUBS = {
      ".rubocop.yml" => <<~YAML,
        inherit_gem:
          rubykatzen-baseline: config/rubocop.yml

        # Generate project-specific excludes, then uncomment inherit_from below:
        #   bundle exec rubocop --auto-gen-config --auto-gen-only-exclude --exclude-limit 10000
        # inherit_from:
        #   - .rubocop_todo.yml
      YAML
      ".erb_lint.yml" => <<~YAML,
        inherit_gem:
          rubykatzen-baseline: config/erb_lint.yml

        # Find cops with violations, then create .erb_lint_todo.yml (see README):
        #   bundle exec erb_lint --lint-all
        # inherit_from:
        #   - .erb_lint_todo.yml
      YAML
    }.freeze

    def initialize(root)
      @root = root
    end

    def call
      STUBS.each do |relative_path, content|
        target = File.join(@root, relative_path)
        if File.exist?(target)
          warn "skip #{relative_path} (already exists)"
          next
        end

        File.write(target, content)
        warn "create #{relative_path}"
      end
    end
  end
end
