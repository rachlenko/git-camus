#!/bin/bash
# Git-Camus Uninstallation Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_message() {
	local color=$1
	local message=$2
	echo -e "${color}${message}${NC}"
}

print_message $BLUE "Uninstalling Git-Camus..."

# Define paths
VENV_DIR="$HOME/.local/venvs/git-camus"
BIN_DIR="$HOME/.local/bin"
SCRIPT_PATH="$BIN_DIR/git-camus"

# Remove virtual environment
if [ -d "$VENV_DIR" ]; then
	print_message $BLUE "Removing virtual environment at $VENV_DIR"
	rm -rf "$VENV_DIR"
else
	print_message $YELLOW "Virtual environment not found at $VENV_DIR"
fi

# Remove wrapper script
if [ -f "$SCRIPT_PATH" ]; then
	print_message $BLUE "Removing wrapper script at $SCRIPT_PATH"
	rm -f "$SCRIPT_PATH"
else
	print_message $YELLOW "Wrapper script not found at $SCRIPT_PATH"
fi

# Check if bin directory is empty and remove if so
if [ -d "$BIN_DIR" ] && [ -z "$(ls -A "$BIN_DIR")" ]; then
	print_message $BLUE "Removing empty directory $BIN_DIR"
	rmdir "$BIN_DIR"
fi

print_message $GREEN "Git-Camus has been successfully uninstalled!"
