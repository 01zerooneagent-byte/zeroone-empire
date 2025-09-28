#!/bin/bash
# 🔄 Auto Git updater for ZeroOne empire

# Fail if no commit message given
if [ -z "$1" ]; then
  echo "❌ Please provide a commit message"
  echo "Usage: ./update_zeroone.sh \"Your commit message\""
  exit 1
fi

cd ~/ZeroOne || exit 1

echo "📂 Inside ZeroOne empire folder"

# Stage all changes
git add .

# Commit with your message
git commit -m "$1"

# Push to main
git push origin main

echo "✅ ZeroOne empire updated on GitHub with message: $1"
