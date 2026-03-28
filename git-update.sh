#!/bin/bash

# vim: ts=3 sw=3 sts=3 sr noet

MAX_LEN=72

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
		commit_msg="$(git diff --cached --name-status)"
	fi

	# Truncate commit message if too long
	if [ ${#commit_msg} -gt $MAX_LEN ]; then
		commit_msg="${commit_msg:0:$MAX_LEN}"
	fi

	git commit -m "$commit_msg"
	git push
fi
