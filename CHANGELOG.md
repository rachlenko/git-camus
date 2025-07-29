# Changelog

## [0.2.0] - 2024-07-29

### Changed
- **BREAKING**: Replaced Anthropic API integration with local Ollama service
- Removed dependency on `ANTHROPIC_API_KEY` environment variable
- Added support for `OLLAMA_HOST` and `OLLAMA_MODEL` environment variables
- Updated all documentation to reflect Ollama setup and usage
- Simplified dependencies to only require `click` and `httpx`

### Added
- Local processing with Ollama for improved privacy
- Support for custom Ollama models (llama3.2, codellama, mistral, etc.)
- Better error handling for Ollama connection issues
- Comprehensive test suite for Ollama integration

### Removed
- Anthropic API dependencies and configuration
- External API calls and associated privacy concerns

## [0.1.0] - 2024-07-29

### Added
- Initial release with Anthropic API integration
- Philosophical commit message generation inspired by Albert Camus
- Command-line interface with show and commit modes
- Support for custom commit message context
