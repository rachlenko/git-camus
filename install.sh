#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    echo "Usage: $0 [--prefix PREFIX]"
    echo ""
    echo "Install git-camus as a standalone utility."
    echo ""
    echo "Options:"
    echo "  --prefix PREFIX   Installation prefix (default: /usr/local)"
    echo "                    The binary will be placed in PREFIX/bin/git-camus"
    echo "  --help            Show this help message"
    exit "${1:-0}"
}

PREFIX="/usr/local"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --prefix)
            PREFIX="$2"
            shift 2
            ;;
        --help|-h)
            usage 0
            ;;
        *)
            echo "Error: unknown option '$1'" >&2
            usage 1
            ;;
    esac
done

LIBDIR="${PREFIX}/lib/git-camus"
BINDIR="${PREFIX}/bin"

echo "Installing git-camus into ${PREFIX} ..."

# Check for Python 3.9+
PYTHON=""
for candidate in python3 python; do
    if command -v "$candidate" &>/dev/null; then
        version=$("$candidate" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        major="${version%%.*}"
        minor="${version#*.}"
        if [[ "$major" -ge 3 && "$minor" -ge 9 ]]; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [[ -z "$PYTHON" ]]; then
    echo "Error: Python 3.9+ is required but not found" >&2
    exit 1
fi

echo "Using $PYTHON ($("$PYTHON" --version))"

# Create directories
mkdir -p "${LIBDIR}" "${BINDIR}"

# Create a virtual environment in the lib directory
echo "Creating virtual environment ..."
"$PYTHON" -m venv "${LIBDIR}/venv"

# Install git-camus into the virtual environment
echo "Installing git-camus package ..."
"${LIBDIR}/venv/bin/pip" install --quiet --upgrade pip
"${LIBDIR}/venv/bin/pip" install --quiet "${SCRIPT_DIR}"

# Create the wrapper script in bin
cat > "${BINDIR}/git-camus" <<'WRAPPER'
#!/usr/bin/env bash
set -euo pipefail
SELF="$(readlink -f "$0" 2>/dev/null || realpath "$0" 2>/dev/null || echo "$0")"
PREFIX="$(dirname "$(dirname "$SELF")")"
exec "${PREFIX}/lib/git-camus/venv/bin/git-camus" "$@"
WRAPPER

chmod +x "${BINDIR}/git-camus"

echo ""
echo "git-camus installed successfully!"
echo "  Binary:  ${BINDIR}/git-camus"
echo "  Library: ${LIBDIR}/venv"
echo ""

# Check if bin is in PATH
if ! echo "$PATH" | tr ':' '\n' | grep -qx "${BINDIR}"; then
    echo "Note: ${BINDIR} is not in your PATH."
    echo "Add it with:  export PATH=\"${BINDIR}:\$PATH\""
fi
