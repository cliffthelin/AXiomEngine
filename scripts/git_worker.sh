#!/bin/bash
# AXIOMENGINE GIT WORKTREE HELPER
# Inspired by pi-git-worktrees.
# Usage: ./git_worker.sh <branch_name> <target_path>

REPO_ROOT="/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine"
BRANCH=$1
TARGET=$2

if [ -z "$BRANCH" ] || [ -z "$TARGET" ]; then
    echo "Usage: $0 <branch_name> <target_path>"
    exit 1
fi

cd "$REPO_ROOT" || exit 1

echo "Creating isolated worktree for branch '$BRANCH' at '$TARGET'..."

# Ensure we are in a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Error: Not a git repository."
    exit 1
fi

# Create the worktree
# This allows the agent to work on a separate branch in a separate folder simultaneously
git worktree add -b "$BRANCH" "$TARGET"

echo "Worktree ready at $TARGET"
echo "Agents can now operate in isolation."
