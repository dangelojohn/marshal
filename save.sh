#!/bin/bash
# Marshal — save everything.
# Usage:  ./save.sh "what changed"
#
# 1. commits to local git
# 2. mirrors a plain copy into ~/Downloads/_backups (survives a bad git operation)
# 3. pushes to Forgejo on the QNAP  (john/marshal, public)

set -euo pipefail
cd "$(dirname "$0")"

MSG="${1:-save $(date '+%Y-%m-%d %H:%M')}"

git add -A
if git diff --cached --quiet; then
  echo "· no changes to commit"
else
  git commit -q -m "$MSG"
  echo "✅ committed: $MSG"
fi

MIRROR="$HOME/Downloads/_backups/marshal-show-latest"
mkdir -p "$MIRROR"
rsync -a --delete --exclude '.git' ./ "$MIRROR/"
echo "✅ mirrored → $MIRROR"

if git remote | grep -qx forgejo; then
  if git push -q forgejo main 2>/dev/null; then
    echo "✅ pushed → forgejo/main"
  else
    # Credential helper didn't cover it — fall back to the stored token.
    TOK=$(grep '192\.168\.68\.108%3a9443' ~/.git-credentials 2>/dev/null \
          | sed -E 's#^https?://([^@]*)@.*#\1#' | cut -d: -f2- \
          | python3 -c 'import sys,urllib.parse;print(urllib.parse.unquote(sys.stdin.read().strip()))' 2>/dev/null || true)
    if [ -n "${TOK:-}" ] && git -c credential.helper= \
         -c "http.extraheader=Authorization: token $TOK" push -q forgejo main; then
      echo "✅ pushed → forgejo/main"
    else
      echo "⚠  push failed — commit and mirror are safe. Check the Forgejo credential."
    fi
  fi
fi

echo
git log --oneline | head -5
