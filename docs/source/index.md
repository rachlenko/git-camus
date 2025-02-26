# Git-Camus Documentation

```{toctree}
:maxdepth: 2
:caption: Contents

installation
usage
api
philosophy
contributing
changelog
```

## Git-Camus: Commit Messages with Existential Flair

Welcome to Git-Camus, a tool that transforms ordinary Git commit messages into philosophical reflections inspired by Albert Camus. 

This documentation will guide you through installation, usage, and the API of Git-Camus.

## Overview

Git-Camus is a command-line tool that:

1. Analyzes your staged Git changes
2. Generates a commit message with existentialist flair 
3. Commits your changes with the generated message

By using Claude AI to generate messages, Git-Camus ensures each commit message is unique, meaningful, and philosophically stimulating.

## Features

- **Philosophical Commit Messages**: Transform mundane commit messages into existentialist reflections
- **Contextual Analysis**: Analyzes your actual code changes for relevant, accurate messages
- **Custom Context**: Provide your own message as context for the generated philosophical message
- **Preview Mode**: View the generated message without committing

## Quick Start

```bash
# Install
pip install git-camus

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Stage your changes
git add .

# Generate a philosophical commit message and commit
git-camus
```

## Indices and Tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
