# API Reference

This page documents the Python API of Git-Camus, which you can use to integrate the functionality into your own tools or workflows.

## Core Functions

### Git Operations

```{eval-rst}
.. py:function:: get_git_diff() -> str

   Retrieve the staged changes in the git repository.

   :return: The output of ``git diff --staged``
   :rtype: str
   :raises SystemExit: If the git command fails
```

```{eval-rst}
.. py:function:: get_git_status() -> str

   Get the current status of the git repository.

   :return: The output of ``git status -s``
   :rtype: str
   :raises SystemExit: If the git command fails
```

```{eval-rst}
.. py:function:: perform_git_commit(message: str) -> None

   Execute a git commit with the provided message.

   :param message: The commit message to use
   :type message: str
   :raises SystemExit: If the git commit command fails
```

### Anthropic API Integration

```{eval-rst}
.. py:function:: generate_commit_message(diff: str, status: str) -> dict

   Format git diff and status for the Anthropic Claude API request.

   :param diff: Output from git diff --staged
   :type diff: str
   :param status: Output from git status -s
   :type status: str
   :return: Request object for the Anthropic API
   :rtype: dict
```

```{eval-rst}
.. py:function:: call_anthropic_api(request_data: dict) -> dict

   Call the Anthropic Claude API to generate a commit message.

   :param request_data: Request data for the Anthropic API
   :type request_data: dict
   :return: The API response
   :rtype: dict
   :raises SystemExit: If the API call fails
```

### Command Line Interface

```{eval-rst}
.. py:function:: main(show: bool, message: Optional[str]) -> None

   Generate an existential commit message in the style of Albert Camus.

   :param show: If True, show the message without committing
   :type show: bool
   :param message: Optional original commit message to enhance
   :type message: Optional[str]
   :raises SystemExit: On various error conditions
```

## Type Definitions

```{eval-rst}
.. py:class:: AnthropicMessage

   Type definition for a Claude API message.

   .. py:attribute:: role
      :type: str

      The role of the message sender (system, user, or assistant)

   .. py:attribute:: content
      :type: str

      The content of the message
```

```{eval-rst}
.. py:class:: AnthropicRequest

   Type definition for an Anthropic API request.

   .. py:attribute:: model
      :type: str

      The Claude model to use

   .. py:attribute:: max_tokens
      :type: int

      Maximum number of tokens in the response

   .. py:attribute:: messages
      :type: List[AnthropicMessage]

      List of messages in the conversation

   .. py:attribute:: temperature
      :type: float

      Temperature setting for generation (0.0-1.0)
```

## Using Git-Camus as a Library

You can use Git-Camus as a library in your Python scripts:

```python
import git_camus

# Get the current git changes
diff = git_camus.get_git_diff()
status = git_camus.get_git_status()

# Generate a request for the Anthropic API
request = git_camus.generate_commit_message(diff, status)

# Call the API to get a philosophical commit message
response = git_camus.call_anthropic_api(request)

# Extract the message
message = response.get("content", [{}])[0].get("text", "").strip()

# Use the message as needed
print(message)
```

This allows you to integrate Git-Camus's functionality into your own tools or workflows.
