# Installation Guide

This guide will walk you through installing Git-Camus and setting up the necessary API credentials.

## Requirements

Before installing Git-Camus, ensure you have:

- Python 3.9 or newer
- Git installed and in your PATH
- An Anthropic API key with access to Claude models

## Installing from PyPI

The simplest way to install Git-Camus is through pip:

```bash
pip install git-camus
```

## Installing from Source

For the latest development version, you can install directly from the GitHub repository:

```bash
git clone https://github.com/rachlenko/git-camus.git
cd git-camus
pip install -e .
```

## Setting Up API Credentials

Git-Camus uses the Anthropic Claude API to generate philosophical commit messages. You'll need to set your API key as an environment variable:

### Linux/macOS

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Add this line to your `~/.bashrc`, `~/.zshrc`, or equivalent shell configuration file to make it persistent.

### Windows (Command Prompt)

```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

### Windows (PowerShell)

```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

To make it persistent in PowerShell, add it to your PowerShell profile:

```powershell
echo '$env:ANTHROPIC_API_KEY="your-api-key-here"' >> $PROFILE
```

## Verifying the Installation

After installation, you can verify that Git-Camus is correctly installed by running:

```bash
git-camus --help
```

You should see the help output showing the available commands and options.

## Troubleshooting

### API Key Issues

If you see errors related to the API key, check that:

1. You've set the `ANTHROPIC_API_KEY` environment variable correctly
2. Your API key is valid and has access to Claude models
3. The environment variable is visible to the process running Git-Camus

### Python Version Issues

If you encounter errors related to Python syntax or imports, check your Python version:

```bash
python --version
```

Git-Camus requires Python 3.9 or newer.

### Git Issues

Git-Camus requires Git to be installed and accessible in your PATH. Verify Git is working:

```bash
git --version
```

### Package Dependencies

If you encounter missing dependency errors, try reinstalling with all dependencies:

```bash
pip install --upgrade git-camus
```

## Next Steps

Now that you have Git-Camus installed, proceed to the [Usage Guide](usage.md) to learn how to use it effectively.
