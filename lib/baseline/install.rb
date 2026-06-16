# frozen_string_literal: true

module Baseline
  class Install
    STUBS = {
      ".rubocop.yml" => <<~YAML,
        inherit_gem:
          rubykatzen-baseline: configs/rubocop.yml

        inherit_from:
          - .rubocop_todo.yml
      YAML
      ".erb_lint.yml" => <<~YAML
        inherit_gem:
          rubykatzen-baseline: configs/erb-lint.yml

        inherit_from:
          - .erb_lint_todo.yml
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
        puts "create #{relative_path}"
      end
    end
  end
end
