# API Reference

This document provides detailed information about the Git-Camus API and its integration with Ollama.

## Core Functions

### Git Operations

#### `get_git_diff() -> str`

Run `git diff --staged` to get the changes to be committed.

**Returns:**
- `str`: The output of git diff showing pending changes.

**Raises:**
- `SystemExit`: If git diff fails or if not in a git repository.

#### `get_git_status() -> str`

Run `git status` to get the repository status.

**Returns:**
- `str`: The output of git status.

**Raises:**
- `SystemExit`: If git status fails or if not in a git repository.

### Ollama API Integration

#### `generate_commit_message(diff: str, status: str) -> OllamaRequest`

Format the git diff and status data for the Ollama API request.

**Parameters:**
- `diff`: The output from git diff --staged
- `status`: The output from git status -s

**Returns:**
- `OllamaRequest`: Request object for the Ollama API

**Example:**
```python
diff = get_git_diff()
status = get_git_status()
request = generate_commit_message(diff, status)
```

#### `call_ollama_api(request_data: OllamaRequest) -> Dict[str, Any]`

Call the local Ollama API to generate a commit message.

**Parameters:**
- `request_data`: Request data for the Ollama API

**Returns:**
- `Dict[str, Any]`: The API response

**Raises:**
- `SystemExit`: If the API call fails

**Example:**
```python
response = call_ollama_api(request_data)
commit_message = response.get("message", {}).get("content", "").strip()
```

### Git Commit Operations

#### `perform_git_commit(message: str) -> None`

Execute git commit with the provided message.

**Parameters:**
- `message`: The commit message to use

**Raises:**
- `SystemExit`: If git commit fails

## Data Types

### OllamaMessage

Type for an Ollama API message.

```python
class OllamaMessage(TypedDict):
    role: str      # "user" or "assistant"
    content: str   # The message content
```

### OllamaRequest

Type definition for an Ollama API request.

```python
class OllamaRequest(TypedDict):
    model: str                    # Model name (e.g., "llama3.2")
    messages: List[OllamaMessage] # List of conversation messages
    stream: bool                  # Whether to stream the response
    options: Dict[str, Any]       # Generation options
```

## Configuration

### Environment Variables

- `OLLAMA_HOST`: Ollama service URL (default: "http://localhost:11434")
- `OLLAMA_MODEL`: Model to use for generation (default: "llama3.2")

### Generation Options

The following options can be set in the `options` field of `OllamaRequest`:

- `temperature`: Controls randomness (0.0-1.0, default: 0.7)
- `top_p`: Nucleus sampling parameter (0.0-1.0, default: 0.9)
- `max_tokens`: Maximum tokens in response (default: 150)

## Example Usage

```python
import git_camus

# Get git information
diff = git_camus.get_git_diff()
status = git_camus.get_git_status()

# Generate a request for the Ollama API
request = git_camus.generate_commit_message(diff, status)

# Call the API
response = git_camus.call_ollama_api(request)

# Extract the commit message
commit_message = response.get("message", {}).get("content", "").strip()

# Commit the changes
git_camus.perform_git_commit(commit_message)
```

## Error Handling

The API functions handle common errors and provide helpful error messages:

- **Git repository errors**: Checks if you're in a git repository
- **Ollama connection errors**: Verifies Ollama is running and accessible
- **Model errors**: Ensures the specified model is available
- **API errors**: Handles HTTP errors and provides debugging information

## Integration with Ollama

Git-Camus integrates with Ollama's chat API endpoint (`/api/chat`) to generate philosophical commit messages. The integration:

1. Formats git changes into a structured prompt
2. Sends the prompt to the local Ollama service
3. Extracts the generated commit message from the response
4. Handles errors gracefully with helpful messages

The prompt is designed to generate commit messages that reflect existentialist philosophy while being relevant to the actual code changes.
