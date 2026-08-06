#!/bin/bash
# Marshal — save everything.
# Usage:  ./save.sh "what changed"
#
# Commits the whole folder to local git and mirrors it into ~/Downloads/_backups.
# No remote is configured, so nothing leaves this machine.

set -euo pipefail
cd "$(dirname "$0")"

MSG="${1:-save $(date '+%Y-%m-%d %H:%M')}"

git add -A
if git diff --cached --quiet; then
  echo "· nothing changed since the last save"
else
  git commit -q -m "$MSG"
  echo "✅ committed: $MSG"
fi

# Mirror a copy out of the project tree, so a bad git operation can't take it too.
MIRROR="$HOME/Downloads/_backups/marshal-show-latest"
mkdir -p "$MIRROR"
rsync -a --delete --exclude '.git' ./ "$MIRROR/"
echo "✅ mirrored → $MIRROR"

echo
echo "saves so far:"
git log --oneline | head -5
