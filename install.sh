#!/bin/bash
# Git-Camus Installation Script

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

print_message $BLUE "Installing Git-Camus..."

# Define paths
VENV_DIR="$HOME/.local/venvs/git-camus"
BIN_DIR="$HOME/.local/bin"
SCRIPT_PATH="$BIN_DIR/git-camus"

# Step 1: Check if venv directory exists and remove/create
if [ -d "$VENV_DIR" ]; then
	print_message $YELLOW "Removing existing virtual environment at $VENV_DIR"
	rm -rf "$VENV_DIR"
fi

print_message $BLUE "Creating new virtual environment at $VENV_DIR"
python -m venv "$VENV_DIR"

# Step 2: Create bin directory if it doesn't exist
if [ ! -d "$BIN_DIR" ]; then
	print_message $BLUE "Creating directory $BIN_DIR"
	mkdir -p "$BIN_DIR"
fi

# Step 3: Create the git-camus shell script
print_message $BLUE "Creating git-camus wrapper script at $SCRIPT_PATH"
cat >"$SCRIPT_PATH" <<'EOF'
#!/bin/bash
# Git-Camus wrapper script

# Source the virtual environment
source "$HOME/.local/venvs/git-camus/bin/activate"

# Run git-camus with all arguments
git-camus "$@"

# Exit
exit 0
EOF

# Make the script executable
chmod +x "$SCRIPT_PATH"

# Step 4: Install git-camus and dependencies
print_message $BLUE "Installing git-camus and dependencies..."

# Activate the virtual environment and install packages
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install git-camus httpx click

print_message $GREEN "Installation completed successfully!"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
	print_message $YELLOW "Warning: $HOME/.local/bin is not in your PATH."
	print_message $YELLOW "Add the following line to your ~/.bashrc or ~/.zshrc:"
	print_message $BLUE "export PATH=\"\$HOME/.local/bin:\$PATH\""
	print_message $YELLOW "Then restart your terminal or run: source ~/.bashrc"
fi

print_message $GREEN "Git-Camus is now installed!"
print_message $BLUE "Usage:"
print_message $BLUE "  git-camus --help"
print_message $BLUE "  git-camus --show"
print_message $BLUE "  git-camus -m \"your message\""
