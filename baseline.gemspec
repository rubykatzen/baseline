# frozen_string_literal: true

require_relative "lib/baseline/version"

Gem::Specification.new do |spec|
  spec.name = "rubykatzen-baseline"
  spec.version = Baseline::VERSION
  spec.authors = ["rubykatzen"]
  spec.summary = "Shared RuboCop and erb_lint configs for dupmachine repositories"
  spec.description = "Packages baseline RuboCop and erb_lint configs with runtime dependencies for consumer Ruby projects."
  spec.homepage = "https://github.com/rubykatzen/baseline"
  spec.license = "MIT"
  spec.required_ruby_version = ">= 3.2"

  spec.files = Dir[
    "config/**/*",
    "lib/**/*",
    "exe/**/*",
    "baseline.gemspec",
    "LICENSE"
  ]

  spec.bindir = "exe"
  spec.executables = ["baseline-install"]
  spec.require_paths = ["lib"]

  spec.add_dependency "rubocop", "~> 1.88"
  spec.add_dependency "rubocop-performance", "~> 1.26"
  spec.add_dependency "rubocop-rails", "~> 2.35"
  spec.add_dependency "standard-custom", "~> 1.0"
  spec.add_dependency "erb_lint", "~> 0.9"
end
