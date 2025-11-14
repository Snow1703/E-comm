#!/bin/bash

# Script to push E-commerce Analytics Dashboard to GitHub
# Usage: ./push_to_github.sh YOUR_REPO_NAME

if [ -z "$1" ]; then
    echo "Usage: ./push_to_github.sh YOUR_REPO_NAME"
    echo "Example: ./push_to_github.sh E-commerce-Analytics-Dashboard"
    exit 1
fi

REPO_NAME=$1
GITHUB_USER="Snow1703"  # Update this if different

echo "🚀 Pushing to GitHub..."
echo "Repository: https://github.com/${GITHUB_USER}/${REPO_NAME}"

# Remove existing remote if any
git remote remove origin 2>/dev/null

# Add new remote
git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git

# Ensure we're on main branch
git branch -M main

# Push to GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "📱 View your repository at: https://github.com/${GITHUB_USER}/${REPO_NAME}"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   1. The repository exists on GitHub"
    echo "   2. You have the correct permissions"
    echo "   3. You're authenticated (git credential helper or SSH key)"
fi

