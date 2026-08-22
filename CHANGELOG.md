# Changelog

## [0.15.0](https://github.com/rubykatzen/baseline/compare/v0.14.0...v0.15.0) (2026-08-22)


### Features

* compact Telegram PR messages ([#165](https://github.com/rubykatzen/baseline/issues/165)) ([6b88491](https://github.com/rubykatzen/baseline/commit/6b884911d5298bba5d1f898a6c3c0b7d654e4f33))
* emphasize repository in Telegram messages ([#168](https://github.com/rubykatzen/baseline/issues/168)) ([f8973e0](https://github.com/rubykatzen/baseline/commit/f8973e01a6c84ffcc0ba6afdadfbdfd0466738b8))

## [0.14.0](https://github.com/rubykatzen/baseline/compare/v0.13.1...v0.14.0) (2026-08-22)


### Features

* add optional Embedder configs ([#162](https://github.com/rubykatzen/baseline/issues/162)) ([dfe6799](https://github.com/rubykatzen/baseline/commit/dfe67995562ce859da3252330d6cdb68dcd09951))

## [0.13.1](https://github.com/rubykatzen/baseline/compare/v0.13.0...v0.13.1) (2026-08-18)


### Bug Fixes

* ignore unsupported reusable workflow context ([#157](https://github.com/rubykatzen/baseline/issues/157)) ([8727b49](https://github.com/rubykatzen/baseline/commit/8727b49e4abff4f513b2dcf03249ac0d53369239))

## [0.13.0](https://github.com/rubykatzen/baseline/compare/v0.12.0...v0.13.0) (2026-08-17)


### Features

* enforce GitHub label descriptions ([#154](https://github.com/rubykatzen/baseline/issues/154)) ([18fe77f](https://github.com/rubykatzen/baseline/commit/18fe77f98e7a728ae5293e462d07ab2280fd4f08))
* standardize repository labels ([#145](https://github.com/rubykatzen/baseline/issues/145)) ([b4bbfe8](https://github.com/rubykatzen/baseline/commit/b4bbfe8fa00ac2da4d5a466f37bfd9198d0f438b))


### Bug Fixes

* keep release markers out of copied examples ([#155](https://github.com/rubykatzen/baseline/issues/155)) ([3c21417](https://github.com/rubykatzen/baseline/commit/3c2141757a27cd653b2b6d08c2781bb9a0e97a4a))

## [0.12.0](https://github.com/rubykatzen/baseline/compare/v0.11.0...v0.12.0) (2026-08-12)


### Features

* add agent message suffix ([ef14507](https://github.com/rubykatzen/baseline/commit/ef145079056809daa94d1b6183a178a73a0ef82e))
* add embedded content checks ([381fef6](https://github.com/rubykatzen/baseline/commit/381fef62d07ce17084b82a1f0ab15a062492b22d))
* add GitHub Copilot agent emoji ([2d7c1df](https://github.com/rubykatzen/baseline/commit/2d7c1dffac927b0209ba5c6036c566e8485c9d59))
* add intake-issue-clarification workflow ([#101](https://github.com/rubykatzen/baseline/issues/101)) ([fde49b6](https://github.com/rubykatzen/baseline/commit/fde49b666391b7bf32037dcd0e5109ff9e99ddec))
* add Release Please workflow ([#132](https://github.com/rubykatzen/baseline/issues/132)) ([0f31544](https://github.com/rubykatzen/baseline/commit/0f3154463216b29ede0b5f4e00deb649cdcb03f8))
* add reusable Telegram notification workflows ([#139](https://github.com/rubykatzen/baseline/issues/139)) ([c3bd9f7](https://github.com/rubykatzen/baseline/commit/c3bd9f7f8af077f45f2db75de6431bfda82721a2))
* add shared GitHub config checks ([7e5487b](https://github.com/rubykatzen/baseline/commit/7e5487bf5c7c1654c837620c04e68381ff2ab8d4))
* add Tombi TOML linting ([#105](https://github.com/rubykatzen/baseline/issues/105)) ([075d4c5](https://github.com/rubykatzen/baseline/commit/075d4c52605cb2be77a9805f2a22aaf4b4e368de))
* add workflow_dispatch trigger to release-finalize ([2135e00](https://github.com/rubykatzen/baseline/commit/2135e000a927917eeb68bd99c0ba67199ece0553))
* align RuboCop style with Ruff, extract config overrides doc ([233b39d](https://github.com/rubykatzen/baseline/commit/233b39dd4f740cd527d1f821ad015195ac154986))
* align RuboCop style with Ruff, extract config overrides doc ([80c329d](https://github.com/rubykatzen/baseline/commit/80c329d9a5403bcda79f534b41cb83e0a4bb2f80))
* auto-detect repository linters ([#107](https://github.com/rubykatzen/baseline/issues/107)) ([fce9341](https://github.com/rubykatzen/baseline/commit/fce9341e9c2f81cb2ceea684481c7d57572a98de))
* bring lint-herb up to full linter pattern ([#85](https://github.com/rubykatzen/baseline/issues/85)) ([e0289a4](https://github.com/rubykatzen/baseline/commit/e0289a493c12a2f897599936f77d21a5ca458533))
* bump pre-commit rev during release, drop Dependabot pre-commit ecosystem ([c324301](https://github.com/rubykatzen/baseline/commit/c32430194be17fb660ed355262a9993c76ee2e41))
* bump pre-commit rev in prepare-release, drop Dependabot pre-commit ecosystem ([08742de](https://github.com/rubykatzen/baseline/commit/08742de4c15a190d0113f03c75a9d1d37469df3e))
* bump pyproject.toml version as part of release commit ([2f5cc0e](https://github.com/rubykatzen/baseline/commit/2f5cc0ec0fcd8f638f548c18fda80d7797b5b376))
* check linters match pre-commit config in lint-shared ([#79](https://github.com/rubykatzen/baseline/issues/79)) ([3f4dcd8](https://github.com/rubykatzen/baseline/commit/3f4dcd86a8fff73a1fa663e0ae34144ccb98b1c3))
* comment todo inherit_from in install stubs with hints ([e076c71](https://github.com/rubykatzen/baseline/commit/e076c7186cc35c96633236ed45a2426e806e76bf))
* enable Style/FrozenStringLiteralComment ([2555239](https://github.com/rubykatzen/baseline/commit/2555239de467ef9dd929cc4a7c2197450f043830))
* extend pre-commit check with file-type coverage ([#81](https://github.com/rubykatzen/baseline/issues/81)) ([186fc0c](https://github.com/rubykatzen/baseline/commit/186fc0cc8b0d5201f64cf38bb8642191cbb4076a))
* inline standard rubocop configs, drop standard gem wrappers ([#30](https://github.com/rubykatzen/baseline/issues/30)) ([251e5b4](https://github.com/rubykatzen/baseline/commit/251e5b4cd7490e34f8a7f3cb178752968d48748d))
* mark baseline-owned fragments ([eaf02b2](https://github.com/rubykatzen/baseline/commit/eaf02b235ce27855efaebe496f4b660bd6b930a8))
* move release actions to releaser, reference rubykatzen/releaser@v0.3.0 ([c7c6dee](https://github.com/rubykatzen/baseline/commit/c7c6dee2ad1df08ca4eee9876ba70dd78e12ec3a))
* parameterize setup-runtimes, add lint-shared reusable workflow ([2ead0ee](https://github.com/rubykatzen/baseline/commit/2ead0eea5c204adade0a3cd568f3f5ab21787939))
* PR-based release flow with composable actions ([f3e5935](https://github.com/rubykatzen/baseline/commit/f3e5935dfcb27567a95408ed97719c67a3aaa172))
* publish baseline Ruby gem for RuboCop and erb_lint ([8c2fa17](https://github.com/rubykatzen/baseline/commit/8c2fa173f31c1344d26b9b19efa895748396fd8b))
* publish baseline Ruby gem for RuboCop and erb_lint configs ([b264d33](https://github.com/rubykatzen/baseline/commit/b264d33453d789c9021afc8617d7b7ce44406a31))
* publish rubykatzen-baseline gem on release ([f00eb83](https://github.com/rubykatzen/baseline/commit/f00eb8363ce2a0a78307e770d3bd7d71dcc1818e))
* **pymarkdown:** enable front-matter extension ([#1](https://github.com/rubykatzen/baseline/issues/1)) ([4b56a63](https://github.com/rubykatzen/baseline/commit/4b56a63e4696804258a8d1507ea2a8fc012ac38d))
* report embedded fragment diffs ([0c8cb89](https://github.com/rubykatzen/baseline/commit/0c8cb899a860cfe088aa731862d8a5c3a62c916f))
* two-phase release via PR (create-release-pr action) ([55b5da4](https://github.com/rubykatzen/baseline/commit/55b5da4fdd762a6ecde9f8c0295d56606b64ffb6))
* validate conventional pull request titles ([#128](https://github.com/rubykatzen/baseline/issues/128)) ([1759fc1](https://github.com/rubykatzen/baseline/commit/1759fc1adf7e31db0c39ef9fc66d73d977a4f8a8))


### Bug Fixes

* add actions: read permission to release job ([343823c](https://github.com/rubykatzen/baseline/commit/343823cf0a39668cba2ba466aa454eb839c5d078))
* address PR review blockers for rubykatzen-baseline gem ([131976f](https://github.com/rubykatzen/baseline/commit/131976fa8670dc1d909a8e855ef10ca576ff9268))
* address PR review for gem hooks, gemspec, and publish ([faa7e0d](https://github.com/rubykatzen/baseline/commit/faa7e0d8af4c8e60d19960d3fa8c5bc105ad076a))
* align changelog with Release Please formatting ([#135](https://github.com/rubykatzen/baseline/issues/135)) ([75ee0fc](https://github.com/rubykatzen/baseline/commit/75ee0fc5812f6dd39d46d15ccc1e30770777339e))
* bump pre-commit rev in example and README during release ([#88](https://github.com/rubykatzen/baseline/issues/88)) ([6f305bf](https://github.com/rubykatzen/baseline/commit/6f305bfe5c9a342164470c20e4717b9618ebec4f))
* check .erb_lint.yml (not deprecated .erb-lint.yml), loosen gem pins ([fab0869](https://github.com/rubykatzen/baseline/commit/fab0869773be44c5a06e89f9bd94f2806e04f558))
* configure git identity before tagging in create-release ([7768ac2](https://github.com/rubykatzen/baseline/commit/7768ac228d5018d2ba560c47b5ea78f912964177))
* disable Bundler lockfile checksums ([#134](https://github.com/rubykatzen/baseline/issues/134)) ([ec76fb1](https://github.com/rubykatzen/baseline/commit/ec76fb1dbcef90a59273a0fe1afa1fdb9aeaa127))
* disable frozen string comments for erb lint ([#46](https://github.com/rubykatzen/baseline/issues/46)) ([2acb98b](https://github.com/rubykatzen/baseline/commit/2acb98b985f5783c19c284df7fe40bd9a2964ab2))
* disable MD022 (blanks-around-headings) ([fba5b67](https://github.com/rubykatzen/baseline/commit/fba5b67a2fb69cfaf16e7446d14e0e4342e8bf53))
* disable MD022 (blanks-around-headings) ([8514f98](https://github.com/rubykatzen/baseline/commit/8514f98a511c2813b799bfaa34a8de326836b9f9))
* disable Release Please labels ([#136](https://github.com/rubykatzen/baseline/issues/136)) ([ebde0f1](https://github.com/rubykatzen/baseline/commit/ebde0f169dade84355842b2bd63dc5ecfae86c5b))
* drop erb_lint version pin — it depends on rubocop &gt;= 1 internally ([10fabfa](https://github.com/rubykatzen/baseline/commit/10fabfa9e48da96bde5390b14e8404c75d190342))
* drop version pins for rubocop-* and standard-custom ([7f32936](https://github.com/rubykatzen/baseline/commit/7f32936659223ad5c333d87e5da6029289aa6f40))
* error on hooks configured but no matching files ([#90](https://github.com/rubykatzen/baseline/issues/90)) ([ca0579b](https://github.com/rubykatzen/baseline/commit/ca0579b91f0704c1541412aa1ab394346df2a3c6))
* force push release branch, handle existing PR ([02f05e7](https://github.com/rubykatzen/baseline/commit/02f05e70e4ecc7c343dfb8831224e736c45b5a5e))
* inherit baseline rubocop config inside erb_lint rubocop_config ([9a8b29d](https://github.com/rubykatzen/baseline/commit/9a8b29dafea0dbc94086af05d3cb82c77e459e36))
* inherit baseline rubocop config inside erb_lint rubocop_config ([5e422ab](https://github.com/rubykatzen/baseline/commit/5e422ab18805ed3b337b9d7ca6fbdda824b71c16))
* make hooks/herb.sh executable ([#27](https://github.com/rubykatzen/baseline/issues/27)) ([745c0d9](https://github.com/rubykatzen/baseline/commit/745c0d99c7c2029274298ff50092b83697818293))
* pass PR branch ref via env var in release-finalize ([fcb3944](https://github.com/rubykatzen/baseline/commit/fcb39441a0a70ba7d1ddd61178a960f070a63a43))
* pin RuboCop 1.88+ and rubocop-rails 2.35+ in baseline gem ([a9ac92c](https://github.com/rubykatzen/baseline/commit/a9ac92c6f857a5e29ae14b72e4e840f49d44e10d))
* pin transitive gem dependencies to minor versions in gemspec ([857b5cc](https://github.com/rubykatzen/baseline/commit/857b5ccadc131dfb8103c5755bdd95d93fd9b34a))
* relax empty-lines max from 0 to 1 ([#97](https://github.com/rubykatzen/baseline/issues/97)) ([b67d8c9](https://github.com/rubykatzen/baseline/commit/b67d8c9c6b3826960250add4937e5f3489982217)), closes [#96](https://github.com/rubykatzen/baseline/issues/96)
* relax yamllint rules for Psych-generated YAML ([#94](https://github.com/rubykatzen/baseline/issues/94)) ([b142bef](https://github.com/rubykatzen/baseline/commit/b142befbe45f09eebac8ebd21a68096508bd5d8a))
* remove blank lines in create-release-pr action ([bfb078d](https://github.com/rubykatzen/baseline/commit/bfb078d38edffce08d58cf941568f1bdb4c3ae90))
* remove blank lines in read-release-data to pass yamllint ([1626af1](https://github.com/rubykatzen/baseline/commit/1626af1b45fe7d172f4316613cc44d4226e44180))
* remove extra blank line in changelog ([7acf6dc](https://github.com/rubykatzen/baseline/commit/7acf6dcddbe6c0cc15e969c8827e0112e4fc9a75))
* remove stale conflict marker from README ([f2602a2](https://github.com/rubykatzen/baseline/commit/f2602a2b94456a4d32b98dc8e6e524781271b134))
* remove trailing comma after last hash item in Install::STUBS ([ed437b1](https://github.com/rubykatzen/baseline/commit/ed437b1615db963b3fa03889e59be5951a3ca932))
* restore Release Please label lifecycle ([#143](https://github.com/rubykatzen/baseline/issues/143)) ([c67d9a4](https://github.com/rubykatzen/baseline/commit/c67d9a4faff31b69ee61e3d14bc93803b7c23ebe))
* set dependabot schedule time to 10:00 ([#92](https://github.com/rubykatzen/baseline/issues/92)) ([ad08400](https://github.com/rubykatzen/baseline/commit/ad08400ce93c23b0ca6fb473af7264bf7064e864))
* silence RuboCop extension tips in shared config ([ceb3b95](https://github.com/rubykatzen/baseline/commit/ceb3b95d805464aa724869c43d04f1253f9472f6))
* tighten gem pins to minor version constraints ([d76fd79](https://github.com/rubykatzen/baseline/commit/d76fd79818fd14bbcac5373071d48d005a01aa1f))
* update Gemfile.lock when bumping gem version on release branch ([6955872](https://github.com/rubykatzen/baseline/commit/6955872ef8371e52f0883a8427675c2a900461cd))
* update verify-release check name to lint / lint ([3edb698](https://github.com/rubykatzen/baseline/commit/3edb698f29f5719458962c323bc38748458ecbc4))
* update verify-release check name to lint / lint ([5fdc5ff](https://github.com/rubykatzen/baseline/commit/5fdc5ff13835e31948315fbdea532567c8002068))
* use HTTPS URLs in pre-commit configs for Dependabot compatibility ([4a61e7a](https://github.com/rubykatzen/baseline/commit/4a61e7aa7b965e20f9cf2d54afe5cfc1b51abfb3))
* use HTTPS URLs in pre-commit configs for Dependabot compatibility ([a70592f](https://github.com/rubykatzen/baseline/commit/a70592f5e295652af89304927ee74dde55380f36))
* use MaximumRangeSize in standard rubocop config ([7eddae1](https://github.com/rubykatzen/baseline/commit/7eddae1c39445b8413ec4eb497c5caee25f84ec5))
* use publish-rubygems action from releaser ([b666e77](https://github.com/rubykatzen/baseline/commit/b666e77c8e066fad191b8456461c51ea54ff1b9a))
* use publish-rubygems action from releaser, closes [#66](https://github.com/rubykatzen/baseline/issues/66) ([7c78283](https://github.com/rubykatzen/baseline/commit/7c78283bf2ecb4f2a94599f7b330324bc23cd025))
* use relative path for pre-commit-autoupdate shared workflow ([d3c0b71](https://github.com/rubykatzen/baseline/commit/d3c0b71faa1a86f055e98ed02c9f76287a25e76a))
* use relative path for pre-commit-autoupdate shared workflow ([cc409a6](https://github.com/rubykatzen/baseline/commit/cc409a66896ec4398b06f52da55ff15fdd739964))

## [0.11.0](https://github.com/rubykatzen/baseline/compare/v0.10.0...v0.11.0) (2026-08-12)


### Features

* add agent message suffix ([ef14507](https://github.com/rubykatzen/baseline/commit/ef145079056809daa94d1b6183a178a73a0ef82e))
* add embedded content checks ([381fef6](https://github.com/rubykatzen/baseline/commit/381fef62d07ce17084b82a1f0ab15a062492b22d))
* add GitHub Copilot agent emoji ([2d7c1df](https://github.com/rubykatzen/baseline/commit/2d7c1dffac927b0209ba5c6036c566e8485c9d59))
* add intake-issue-clarification workflow ([#101](https://github.com/rubykatzen/baseline/issues/101)) ([fde49b6](https://github.com/rubykatzen/baseline/commit/fde49b666391b7bf32037dcd0e5109ff9e99ddec))
* add Release Please workflow ([#132](https://github.com/rubykatzen/baseline/issues/132)) ([0f31544](https://github.com/rubykatzen/baseline/commit/0f3154463216b29ede0b5f4e00deb649cdcb03f8))
* add reusable Telegram notification workflows ([#139](https://github.com/rubykatzen/baseline/issues/139)) ([c3bd9f7](https://github.com/rubykatzen/baseline/commit/c3bd9f7f8af077f45f2db75de6431bfda82721a2))
* add shared GitHub config checks ([7e5487b](https://github.com/rubykatzen/baseline/commit/7e5487bf5c7c1654c837620c04e68381ff2ab8d4))
* add Tombi TOML linting ([#105](https://github.com/rubykatzen/baseline/issues/105)) ([075d4c5](https://github.com/rubykatzen/baseline/commit/075d4c52605cb2be77a9805f2a22aaf4b4e368de))
* add workflow_dispatch trigger to release-finalize ([2135e00](https://github.com/rubykatzen/baseline/commit/2135e000a927917eeb68bd99c0ba67199ece0553))
* align RuboCop style with Ruff, extract config overrides doc ([233b39d](https://github.com/rubykatzen/baseline/commit/233b39dd4f740cd527d1f821ad015195ac154986))
* align RuboCop style with Ruff, extract config overrides doc ([80c329d](https://github.com/rubykatzen/baseline/commit/80c329d9a5403bcda79f534b41cb83e0a4bb2f80))
* auto-detect repository linters ([#107](https://github.com/rubykatzen/baseline/issues/107)) ([fce9341](https://github.com/rubykatzen/baseline/commit/fce9341e9c2f81cb2ceea684481c7d57572a98de))
* bring lint-herb up to full linter pattern ([#85](https://github.com/rubykatzen/baseline/issues/85)) ([e0289a4](https://github.com/rubykatzen/baseline/commit/e0289a493c12a2f897599936f77d21a5ca458533))
* bump pre-commit rev during release, drop Dependabot pre-commit ecosystem ([c324301](https://github.com/rubykatzen/baseline/commit/c32430194be17fb660ed355262a9993c76ee2e41))
* bump pre-commit rev in prepare-release, drop Dependabot pre-commit ecosystem ([08742de](https://github.com/rubykatzen/baseline/commit/08742de4c15a190d0113f03c75a9d1d37469df3e))
* bump pyproject.toml version as part of release commit ([2f5cc0e](https://github.com/rubykatzen/baseline/commit/2f5cc0ec0fcd8f638f548c18fda80d7797b5b376))
* check linters match pre-commit config in lint-shared ([#79](https://github.com/rubykatzen/baseline/issues/79)) ([3f4dcd8](https://github.com/rubykatzen/baseline/commit/3f4dcd86a8fff73a1fa663e0ae34144ccb98b1c3))
* comment todo inherit_from in install stubs with hints ([e076c71](https://github.com/rubykatzen/baseline/commit/e076c7186cc35c96633236ed45a2426e806e76bf))
* enable Style/FrozenStringLiteralComment ([2555239](https://github.com/rubykatzen/baseline/commit/2555239de467ef9dd929cc4a7c2197450f043830))
* extend pre-commit check with file-type coverage ([#81](https://github.com/rubykatzen/baseline/issues/81)) ([186fc0c](https://github.com/rubykatzen/baseline/commit/186fc0cc8b0d5201f64cf38bb8642191cbb4076a))
* inline standard rubocop configs, drop standard gem wrappers ([#30](https://github.com/rubykatzen/baseline/issues/30)) ([251e5b4](https://github.com/rubykatzen/baseline/commit/251e5b4cd7490e34f8a7f3cb178752968d48748d))
* mark baseline-owned fragments ([eaf02b2](https://github.com/rubykatzen/baseline/commit/eaf02b235ce27855efaebe496f4b660bd6b930a8))
* move release actions to releaser, reference rubykatzen/releaser@v0.3.0 ([c7c6dee](https://github.com/rubykatzen/baseline/commit/c7c6dee2ad1df08ca4eee9876ba70dd78e12ec3a))
* parameterize setup-runtimes, add lint-shared reusable workflow ([2ead0ee](https://github.com/rubykatzen/baseline/commit/2ead0eea5c204adade0a3cd568f3f5ab21787939))
* PR-based release flow with composable actions ([f3e5935](https://github.com/rubykatzen/baseline/commit/f3e5935dfcb27567a95408ed97719c67a3aaa172))
* publish baseline Ruby gem for RuboCop and erb_lint ([8c2fa17](https://github.com/rubykatzen/baseline/commit/8c2fa173f31c1344d26b9b19efa895748396fd8b))
* publish baseline Ruby gem for RuboCop and erb_lint configs ([b264d33](https://github.com/rubykatzen/baseline/commit/b264d33453d789c9021afc8617d7b7ce44406a31))
* publish rubykatzen-baseline gem on release ([f00eb83](https://github.com/rubykatzen/baseline/commit/f00eb8363ce2a0a78307e770d3bd7d71dcc1818e))
* **pymarkdown:** enable front-matter extension ([#1](https://github.com/rubykatzen/baseline/issues/1)) ([4b56a63](https://github.com/rubykatzen/baseline/commit/4b56a63e4696804258a8d1507ea2a8fc012ac38d))
* report embedded fragment diffs ([0c8cb89](https://github.com/rubykatzen/baseline/commit/0c8cb899a860cfe088aa731862d8a5c3a62c916f))
* two-phase release via PR (create-release-pr action) ([55b5da4](https://github.com/rubykatzen/baseline/commit/55b5da4fdd762a6ecde9f8c0295d56606b64ffb6))
* validate conventional pull request titles ([#128](https://github.com/rubykatzen/baseline/issues/128)) ([1759fc1](https://github.com/rubykatzen/baseline/commit/1759fc1adf7e31db0c39ef9fc66d73d977a4f8a8))


### Bug Fixes

* add actions: read permission to release job ([343823c](https://github.com/rubykatzen/baseline/commit/343823cf0a39668cba2ba466aa454eb839c5d078))
* address PR review blockers for rubykatzen-baseline gem ([131976f](https://github.com/rubykatzen/baseline/commit/131976fa8670dc1d909a8e855ef10ca576ff9268))
* address PR review for gem hooks, gemspec, and publish ([faa7e0d](https://github.com/rubykatzen/baseline/commit/faa7e0d8af4c8e60d19960d3fa8c5bc105ad076a))
* align changelog with Release Please formatting ([#135](https://github.com/rubykatzen/baseline/issues/135)) ([75ee0fc](https://github.com/rubykatzen/baseline/commit/75ee0fc5812f6dd39d46d15ccc1e30770777339e))
* bump pre-commit rev in example and README during release ([#88](https://github.com/rubykatzen/baseline/issues/88)) ([6f305bf](https://github.com/rubykatzen/baseline/commit/6f305bfe5c9a342164470c20e4717b9618ebec4f))
* check .erb_lint.yml (not deprecated .erb-lint.yml), loosen gem pins ([fab0869](https://github.com/rubykatzen/baseline/commit/fab0869773be44c5a06e89f9bd94f2806e04f558))
* configure git identity before tagging in create-release ([7768ac2](https://github.com/rubykatzen/baseline/commit/7768ac228d5018d2ba560c47b5ea78f912964177))
* disable Bundler lockfile checksums ([#134](https://github.com/rubykatzen/baseline/issues/134)) ([ec76fb1](https://github.com/rubykatzen/baseline/commit/ec76fb1dbcef90a59273a0fe1afa1fdb9aeaa127))
* disable frozen string comments for erb lint ([#46](https://github.com/rubykatzen/baseline/issues/46)) ([2acb98b](https://github.com/rubykatzen/baseline/commit/2acb98b985f5783c19c284df7fe40bd9a2964ab2))
* disable MD022 (blanks-around-headings) ([fba5b67](https://github.com/rubykatzen/baseline/commit/fba5b67a2fb69cfaf16e7446d14e0e4342e8bf53))
* disable MD022 (blanks-around-headings) ([8514f98](https://github.com/rubykatzen/baseline/commit/8514f98a511c2813b799bfaa34a8de326836b9f9))
* disable Release Please labels ([#136](https://github.com/rubykatzen/baseline/issues/136)) ([ebde0f1](https://github.com/rubykatzen/baseline/commit/ebde0f169dade84355842b2bd63dc5ecfae86c5b))
* drop erb_lint version pin — it depends on rubocop &gt;= 1 internally ([10fabfa](https://github.com/rubykatzen/baseline/commit/10fabfa9e48da96bde5390b14e8404c75d190342))
* drop version pins for rubocop-* and standard-custom ([7f32936](https://github.com/rubykatzen/baseline/commit/7f32936659223ad5c333d87e5da6029289aa6f40))
* error on hooks configured but no matching files ([#90](https://github.com/rubykatzen/baseline/issues/90)) ([ca0579b](https://github.com/rubykatzen/baseline/commit/ca0579b91f0704c1541412aa1ab394346df2a3c6))
* force push release branch, handle existing PR ([02f05e7](https://github.com/rubykatzen/baseline/commit/02f05e70e4ecc7c343dfb8831224e736c45b5a5e))
* inherit baseline rubocop config inside erb_lint rubocop_config ([9a8b29d](https://github.com/rubykatzen/baseline/commit/9a8b29dafea0dbc94086af05d3cb82c77e459e36))
* inherit baseline rubocop config inside erb_lint rubocop_config ([5e422ab](https://github.com/rubykatzen/baseline/commit/5e422ab18805ed3b337b9d7ca6fbdda824b71c16))
* make hooks/herb.sh executable ([#27](https://github.com/rubykatzen/baseline/issues/27)) ([745c0d9](https://github.com/rubykatzen/baseline/commit/745c0d99c7c2029274298ff50092b83697818293))
* pass PR branch ref via env var in release-finalize ([fcb3944](https://github.com/rubykatzen/baseline/commit/fcb39441a0a70ba7d1ddd61178a960f070a63a43))
* pin RuboCop 1.88+ and rubocop-rails 2.35+ in baseline gem ([a9ac92c](https://github.com/rubykatzen/baseline/commit/a9ac92c6f857a5e29ae14b72e4e840f49d44e10d))
* pin transitive gem dependencies to minor versions in gemspec ([857b5cc](https://github.com/rubykatzen/baseline/commit/857b5ccadc131dfb8103c5755bdd95d93fd9b34a))
* relax empty-lines max from 0 to 1 ([#97](https://github.com/rubykatzen/baseline/issues/97)) ([b67d8c9](https://github.com/rubykatzen/baseline/commit/b67d8c9c6b3826960250add4937e5f3489982217)), closes [#96](https://github.com/rubykatzen/baseline/issues/96)
* relax yamllint rules for Psych-generated YAML ([#94](https://github.com/rubykatzen/baseline/issues/94)) ([b142bef](https://github.com/rubykatzen/baseline/commit/b142befbe45f09eebac8ebd21a68096508bd5d8a))
* remove blank lines in create-release-pr action ([bfb078d](https://github.com/rubykatzen/baseline/commit/bfb078d38edffce08d58cf941568f1bdb4c3ae90))
* remove blank lines in read-release-data to pass yamllint ([1626af1](https://github.com/rubykatzen/baseline/commit/1626af1b45fe7d172f4316613cc44d4226e44180))
* remove extra blank line in changelog ([7acf6dc](https://github.com/rubykatzen/baseline/commit/7acf6dcddbe6c0cc15e969c8827e0112e4fc9a75))
* remove stale conflict marker from README ([f2602a2](https://github.com/rubykatzen/baseline/commit/f2602a2b94456a4d32b98dc8e6e524781271b134))
* remove trailing comma after last hash item in Install::STUBS ([ed437b1](https://github.com/rubykatzen/baseline/commit/ed437b1615db963b3fa03889e59be5951a3ca932))
* set dependabot schedule time to 10:00 ([#92](https://github.com/rubykatzen/baseline/issues/92)) ([ad08400](https://github.com/rubykatzen/baseline/commit/ad08400ce93c23b0ca6fb473af7264bf7064e864))
* silence RuboCop extension tips in shared config ([ceb3b95](https://github.com/rubykatzen/baseline/commit/ceb3b95d805464aa724869c43d04f1253f9472f6))
* tighten gem pins to minor version constraints ([d76fd79](https://github.com/rubykatzen/baseline/commit/d76fd79818fd14bbcac5373071d48d005a01aa1f))
* update Gemfile.lock when bumping gem version on release branch ([6955872](https://github.com/rubykatzen/baseline/commit/6955872ef8371e52f0883a8427675c2a900461cd))
* update verify-release check name to lint / lint ([3edb698](https://github.com/rubykatzen/baseline/commit/3edb698f29f5719458962c323bc38748458ecbc4))
* update verify-release check name to lint / lint ([5fdc5ff](https://github.com/rubykatzen/baseline/commit/5fdc5ff13835e31948315fbdea532567c8002068))
* use HTTPS URLs in pre-commit configs for Dependabot compatibility ([4a61e7a](https://github.com/rubykatzen/baseline/commit/4a61e7aa7b965e20f9cf2d54afe5cfc1b51abfb3))
* use HTTPS URLs in pre-commit configs for Dependabot compatibility ([a70592f](https://github.com/rubykatzen/baseline/commit/a70592f5e295652af89304927ee74dde55380f36))
* use MaximumRangeSize in standard rubocop config ([7eddae1](https://github.com/rubykatzen/baseline/commit/7eddae1c39445b8413ec4eb497c5caee25f84ec5))
* use publish-rubygems action from releaser ([b666e77](https://github.com/rubykatzen/baseline/commit/b666e77c8e066fad191b8456461c51ea54ff1b9a))
* use publish-rubygems action from releaser, closes [#66](https://github.com/rubykatzen/baseline/issues/66) ([7c78283](https://github.com/rubykatzen/baseline/commit/7c78283bf2ecb4f2a94599f7b330324bc23cd025))
* use relative path for pre-commit-autoupdate shared workflow ([d3c0b71](https://github.com/rubykatzen/baseline/commit/d3c0b71faa1a86f055e98ed02c9f76287a25e76a))
* use relative path for pre-commit-autoupdate shared workflow ([cc409a6](https://github.com/rubykatzen/baseline/commit/cc409a66896ec4398b06f52da55ff15fdd739964))

## [0.10.0](https://github.com/rubykatzen/baseline/compare/v0.9.0...v0.10.0) (2026-08-12)


### Features

* add Release Please workflow ([#132](https://github.com/rubykatzen/baseline/issues/132)) ([0f31544](https://github.com/rubykatzen/baseline/commit/0f3154463216b29ede0b5f4e00deb649cdcb03f8))
* add reusable Telegram notification workflows ([#139](https://github.com/rubykatzen/baseline/issues/139)) ([c3bd9f7](https://github.com/rubykatzen/baseline/commit/c3bd9f7f8af077f45f2db75de6431bfda82721a2))


### Bug Fixes

* align changelog with Release Please formatting ([#135](https://github.com/rubykatzen/baseline/issues/135)) ([75ee0fc](https://github.com/rubykatzen/baseline/commit/75ee0fc5812f6dd39d46d15ccc1e30770777339e))
* disable Bundler lockfile checksums ([#134](https://github.com/rubykatzen/baseline/issues/134)) ([ec76fb1](https://github.com/rubykatzen/baseline/commit/ec76fb1dbcef90a59273a0fe1afa1fdb9aeaa127))
* disable Release Please labels ([#136](https://github.com/rubykatzen/baseline/issues/136)) ([ebde0f1](https://github.com/rubykatzen/baseline/commit/ebde0f169dade84355842b2bd63dc5ecfae86c5b))

## [v0.9.0] - 2026-08-12

* chore(deps): bump rubocop-rails from 2.35.4 to 2.36.0 (#122)
* chore(deps): bump rubocop from 1.88.0 to 1.89.0 (#123)
* chore(deps): bump herb from 0.10.1 to 0.10.3 (#124)
* ci: trust pull request title validation (#130)
* ci: bootstrap trusted pull request validation (#129)
* feat: validate conventional pull request titles (#128)

## [v0.8.6] - 2026-08-12

* feat: add GitHub Copilot agent emoji
* feat: add agent message suffix
* refactor: merge embedded fragment guidance
* chore: disable Dependabot labels
* feat: report embedded fragment diffs
* feat: mark baseline-owned fragments
* refactor: rename GitHub config root
* feat: add embedded content checks

## [v0.8.5] - 2026-08-11

* feat: add shared GitHub config checks

## [v0.8.4] - 2026-08-11

* ci: use self-repository action references
* refactor: rename lint skip input

## [v0.8.3] - 2026-08-11

* ci: enable Tombi linting (#113)

## [v0.8.2] - 2026-08-11

* feat: add Tombi TOML linting (#105)
* chore: pin JSON actions to v0.8 (#111)

## [v0.8.1] - 2026-08-11

* refactor: use JSON linter selection contract (#109)

## [v0.8.0] - 2026-08-11

* feat: auto-detect repository linters (#107)
* chore: remove intake-issue-clarification.yml push-model caller
* feat: add intake-issue-clarification workflow (#101)

## [v0.7.8] - 2026-07-08

* fix: relax empty-lines max from 0 to 1 (#97)

## [v0.7.7] - 2026-07-03

* fix: relax yamllint rules for Psych-generated YAML (#94)
* fix: set dependabot schedule time to 10:00 (#92)

## [v0.7.6] - 2026-07-02

* fix: error on hooks configured but no matching files (#90)

## [v0.7.5] - 2026-07-02

* fix: bump pre-commit rev in example and README during release (#88)

## [v0.7.4] - 2026-07-02

* feat: bring lint-herb up to full linter pattern (#85)
* docs: update README for lint-shared.yml and pre-commit linter (#83)
* chore: remove merge-dependabot-pr workflow (#84)

## [v0.7.3] - 2026-07-02

* feat: extend pre-commit check with file-type coverage (#81)

## [v0.7.2] - 2026-06-24

* feat: check linters match pre-commit config in lint-shared (#79)

## [v0.7.1] - 2026-06-22

* chore: remove ruff and erb-lint, no Python or ERB files in repo
* chore: run merge-dependabot-pr only for dependabot[bot]
* fix: use publish-rubygems action from releaser, closes #66
* chore(deps): bump nokogiri from 1.19.3 to 1.19.4
* chore: reschedule Telegram notify to 10:00 Berlin (08:00 UTC)
* chore: bump releaser to v0.5

## [v0.7.0] - 2026-06-22

No changes

## [v0.6.2] - 2026-06-20

* fix: disable MD022 (blanks-around-headings)

## [v0.6.1] - 2026-06-20

* chore: bump releaser to v0.4.5
* chore: bump releaser to v0.4.4, drop manual Gemfile.lock step
* fix: update Gemfile.lock when bumping gem version on release branch

## [v0.6.0] - 2026-06-20

* refactor: require baseline gem for ruby linting (#47)

## [v0.5.4] - 2026-06-19

* feat: publish baseline Ruby gem with RuboCop and erb_lint configs
* feat: comment out todo inherit_from in install stubs with generation hints
* fix: skip gem-delegating rubocop and erb_lint hooks when no target files
* fix: remove stale gem artifacts before RubyGems publish
* fix: silence RuboCop extension suggestions in shared config
* fix: generate `.erb_lint.yml` stub instead of deprecated `.erb-lint.yml`
* fix: pin RuboCop 1.88+ to match standard config parameters

## [v0.5.3] - 2026-06-19

* lint: disable pymarkdown pragma suppressions (#51)
* erb-lint: skip vendor with project config (#45)

## [v0.5.2] - 2026-06-18

* lint: allow markdown fragments without h1 (#49)
* chore(deps): bump actions/checkout from 6 to 7
* fix: disable frozen string comments for erb lint (#46)
* docs: add portable agent message prefix

## [v0.5.1] - 2026-06-17

* refactor: move bump-pre-commit-rev into local composite action
* feat: bump pre-commit rev in prepare-release, drop Dependabot pre-commit ecosystem
* chore(deps): bump https://github.com/rubykatzen/baseline
* fix: remove stale conflict marker from README
* Replace pre-commit autoupdate workflow with Dependabot.
* docs: add erb_lint todo file format and creation instructions
* fix: inherit baseline rubocop config inside erb_lint rubocop_config
* fix: pin transitive gem dependencies to minor versions in gemspec
* fix: use HTTPS URLs in pre-commit configs for Dependabot compatibility

## [v0.5.0] - 2026-06-17

* chore: bump releaser to v0.3.4
* fix: remove trailing comma after last hash item in Install::STUBS
* fix: address PR review for gem hooks, gemspec, and publish
* feat: comment todo inherit_from in install stubs with hints
* fix: address PR review blockers for rubykatzen-baseline gem
* feat: enable Style/FrozenStringLiteralComment
* rename configs/ to config/ to follow Ruby gem conventions
* rename configs/erb-lint.yml to configs/erb_lint.yml for consistency
* feat: publish rubykatzen-baseline gem on release
* rename gem to rubykatzen-baseline
* chore: bump releaser to v0.3.3, add bump-ruby-gem-version to release flow
* fix: drop erb_lint version pin — it depends on rubocop >= 1 internally
* fix: drop version pins for rubocop-* and standard-custom
* fix: tighten gem pins to minor version constraints
* fix: check .erb_lint.yml (not deprecated .erb-lint.yml), loosen gem pins
* docs: note RuboCop version pins in changelog
* fix: pin RuboCop 1.88+ and rubocop-rails 2.35+ in baseline gem
* fix: silence RuboCop extension tips in shared config
* fix: use MaximumRangeSize in standard rubocop config
* feat: publish baseline Ruby gem for RuboCop and erb_lint configs

## [v0.4.10] - 2026-06-16

* feat: inline standard rubocop configs, drop standard gem wrappers (#30)

## [v0.4.9] - 2026-06-16

* fix: make hooks/herb.sh executable (#27)

## [v0.4.8] - 2026-06-16

* setup-ruby: enable bundler cache when Gemfile is present (#24)

## [v0.4.7] - 2026-06-16

* herb: add lint-herb action (#22)

## [v0.4.6] - 2026-06-16

* erb-lint: use find to collect files, drop --lint-all (#20)

## [v0.4.5] - 2026-06-16

* erb-lint: exclude vendor from linting (#18)
* Update README to generalize workflow description
* chore: remove release actions moved to rubykatzen/releaser (#17)

## [v0.4.4] - 2026-06-15

* docs: replace manual workflow dispatch with releaser CLI in release docs
* docs: add concrete release command example to AGENTS.md
* docs: add link to rubykatzen/releaser in AGENTS.md
* docs: remove dependabot-automerge and telegram workflows from public docs
* Skip hooks when no targets exist (#15)
* docs: document release flow and branch protection
* fix: use relative path for pre-commit-autoupdate shared workflow
* fix portable sed in mise.toml parsing, trap cleanup, and README accuracy
* simplify Ruby linting: setup-ruby handles bundle install, linters detect Gemfile
* chore(deps): bump rubykatzen/baseline/.github/workflows/pre-commit-autoupdate-shared.yml
* use bundle install in Ruby linter actions, remove BASELINE_RUBY_LINTER_STANDALONE
* extract setup-ruby action and add guard steps to Ruby linters
* chore(deps): bump rubykatzen/releaser from 0.3.0 to 0.3.1
* rubocop: exclude vendor from linting
* make Ruby linter actions self-contained

## [v0.4.3] - 2026-06-15

* fix Ruby pre-commit hook file handling

## [v0.4.2] - 2026-06-15

* add Ruby linters: rubocop and erb-lint

## [v0.4.1] - 2026-06-15

* chore: reference telegram-notify and dependabot-automerge from rubykatzen/releaser@v0.3.1

## [v0.4.0] - 2026-06-15

* feat: move release actions to releaser, reference rubykatzen/releaser@v0.3.0

## [v0.3.0] - 2026-06-15

* fix: remove blank lines in read-release-data to pass yamllint
* feat: PR-based release flow with composable actions

## [v0.2.3] - 2026-06-14

* refactor: split pyproject version bump into separate action

## [v0.2.2] - 2026-06-14

* refactor: revert to simple release flow, remove PR-based approach

## [v0.2.1] - 2026-06-14

* fix: force push release branch, handle existing PR
* fix: pass PR branch ref via env var in release-finalize
* fix: remove blank lines in create-release-pr action
* feat: two-phase release via PR (create-release-pr action)
* fix: add actions: read permission to release job

## [v0.2.0] - 2026-06-14

Replace `release-shared.yml` reusable workflow with four composable composite actions: `verify-release`, `generate-notes`, `commit-changelog`, `create-release`. Each action handles one concern and can be used independently. `baseline/release.yml` uses relative action refs to avoid self-reference pinning issues.

## [v0.1.1] - 2026-06-14

Release workflow switched to `workflow_dispatch` trigger with `release-shared.yml` reusable workflow. The shared release workflow now also bumps `version` in `pyproject.toml` (if present) as part of the changelog commit, enabling Homebrew-compatible Python packages.

## [v0.1.0] - 2026-06-14

Added `release-shared.yml` reusable workflow implementing the CI-owned release process: verifies base SHA, checks CI, generates AI release notes, commits changelog, creates tag and GitHub Release. Stripped CHANGELOG mutation from the `create-release` composite action.

## [v0.0.14] - 2026-06-13

* document separate artifact upload after create-release
* chore: update changelog for v0.0.13

## [v0.0.13] - 2026-06-13

* remove artifact-path from create-release action
* rename self-calling workflows to -self suffix; add dependabot-automerge-self; document convention
* add pre-commit config and self-update workflow
* restore telegram-release-notify reusable workflow; add notify-release for baseline self
* add dependabot and telegram-release-notify workflows
* document default schedules and pre-commit autoupdate in README
* chore: update changelog for v0.0.12

## [v0.0.12] - 2026-06-13

* add pre-commit-autoupdate reusable workflow
* use VERSION placeholder instead of pinned version in README
* update README and AGENTS.md with reusable workflows and current version
* chore: update changelog for v0.0.11

## [v0.0.11] - 2026-06-13

* fix changelog trailing newline in create-release action
* remove latest mutable tag from create-release action
* chore: update changelog for v0.0.10

## [v0.0.10] - 2026-06-13

* fix CHANGELOG (last manual fix — action is now patched)
* fix changelog update to preserve # Changelog header position
* chore: update changelog for v0.0.9

## [v0.0.9] - 2026-06-13

* fix changelog update to preserve # Changelog header position
* rename workflows to dependabot-automerge and telegram-release-notify
* fix CHANGELOG structure after merge conflict
* install shellcheck from stable release to get --rcfile support
* fix yamllint empty-lines violations
* add dependabot-automerge and telegram-release-notify reusable workflows
* add UP, B, SIM rules to ruff config

## [v0.0.6] - 2026-06-12

* replace linter reusable workflows with composite actions

## [v0.0.5] - 2026-06-12

* extract create-release composite action, remove publish-app-bundle

## [v0.0.3] - 2026-06-12

* add publish-app-bundle action and AI-generated release notes
