# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-10

### Changed
- Improved dependency file handling
  - Optimized performance by separating dependency and non-dependency changes
  - Reduced token usage by not including full dependency file diffs
  - Enhanced commit message format for dependency updates
- Enhanced code structure
  - Improved type safety with better type annotations
  - Clearer function interfaces and return values
  - Better separation of concerns in code processing

## [0.1.2] - 2025-01-09

### Changed
- Improved model management functionality
  - Simplified `aimsg init` command to show a clear list of models with current selection
  - Enhanced `aimsg model list` command to group models by providers with descriptions
  - Removed redundant `model use` and `model select` commands in favor of `init`
- Updated documentation
  - Added comprehensive API endpoint list for all supported models
  - Reorganized model list in README.md
  - Improved custom model configuration examples

## [0.1.1] - Previous Release

### Added
- Initial release with basic functionality
- Support for multiple AI models:
  - OpenAI GPT models
  - Anthropic Claude models
  - Google PaLM & Gemini
  - Various Chinese models
  - Third-party hosted models
- Custom model support
- Environment variable configuration
- Basic CLI commands:
  - `aimsg init`: Initialize configuration
  - `aimsg commit`: Generate commit message
  - `aimsg model`: Manage AI models

[0.2.0]: https://github.com/yurentle/aimsg/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/yurentle/aimsg/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/yurentle/aimsg/releases/tag/v0.1.1
