#!/bin/bash

# vim: ts=3 sw=3 sts=3 sr noet

# Change into the directory of this script
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

# Add all the files
git add -A


if git diff --staged --quiet; then
  echo "No changes"
else
	if [ $# -eq 1 ]; then
		commit_msg="$1"
	else
		commit_msg="Auto-update $(date) Commit: $(git diff --cached --name-status)"
	fi
	git commit -m "$commit_msg"
	git push
fi
