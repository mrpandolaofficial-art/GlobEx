#!/bin/bash

# Navigate to the script's directory (just in case)
cd "$(dirname "$0")"

if [ -z "$1" ]
then
  echo "❌ Error: Please provide a commit message."
  exit 1
fi

git add .
git commit -m "$1"
git push origin main

echo "✅ GitHub successfully updated!"