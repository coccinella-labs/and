#!/bin/bash

# Script to create and publish an alpha release

set -e

# Read current version
version=$(cat version.txt)

# Create alpha version
alpha_version="${version}-alpha"

# Update version.txt for next
echo "$version" > version.txt  # Keep same for now, or increment

# Commit version change
git add version.txt
git commit -m "chore: bump version to $alpha_version" || true

# Create tag
git tag "v$alpha_version"

# Push tag
git push origin main
git push origin "v$alpha_version"

# Create GitHub release
gh release create "v$alpha_version" --generate-notes --prerelease --title "Alpha Release $alpha_version"

echo "Alpha release $alpha_version published!"