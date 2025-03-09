#!/bin/bash

# Read the current version
VERSION=$(cat VERSION)

# Increment the version
NEW_VERSION=$((VERSION + 1))

# Update the VERSION file
echo "$NEW_VERSION" > VERSION

# Commit and tag
git add VERSION
git commit -m "Release version $NEW_VERSION"
git tag "$NEW_VERSION"
git push origin main #or master
git push origin "$NEW_VERSION"

# Optional: Create release notes on GitHub (using the GitHub CLI or API)
# Example using github CLI:
# gh release create $NEW_VERSION --title "Release $NEW_VERSION" --notes "Here are the release notes."

echo "Released version $NEW_VERSION"