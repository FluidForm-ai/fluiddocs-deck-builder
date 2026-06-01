#!/usr/bin/env bash
# save-locally.sh
# Opens a generated deck HTML file in the user's default browser.
# Cross-platform fallback for the local save path. Never fails.
#
# Usage:
#   ./save-locally.sh path/to/deck.html
#   ./save-locally.sh path/to/deck.html ~/Desktop
#
# Argument 1 (required): path to the generated HTML file.
# Argument 2 (optional): destination directory. Defaults to the file's current location.

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <path-to-deck.html> [destination-dir]"
  exit 1
fi

SRC="$1"
if [ ! -f "$SRC" ]; then
  echo "Error: file not found: $SRC"
  exit 1
fi

DEST_DIR="${2:-$(dirname "$SRC")}"
mkdir -p "$DEST_DIR"

FILENAME="$(basename "$SRC")"
DEST="$DEST_DIR/$FILENAME"

# If src and dest are the same file, skip the copy
if [ "$(realpath "$SRC")" != "$(realpath "$DEST")" ]; then
  cp "$SRC" "$DEST"
fi

# Open in default browser. Cross-platform fallback ladder.
if command -v open >/dev/null 2>&1; then
  open "$DEST"                        # macOS
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$DEST"                    # Linux
elif command -v start >/dev/null 2>&1; then
  start "$DEST"                       # Windows (git-bash, WSL)
else
  echo "Saved to: $DEST"
  echo "Open it manually in your browser."
  exit 0
fi

echo "Deck saved and opened: $DEST"
