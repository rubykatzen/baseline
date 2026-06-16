# frozen_string_literal: true

require_relative "baseline/version"

module Baseline
  def self.gem_root
    File.expand_path("..", __dir__)
  end

  def self.rubocop_config_path
    File.join(gem_root, "config/rubocop.yml")
  end

  def self.erb_lint_config_path
    File.join(gem_root, "config/erb_lint.yml")
  end
end
