#!/usr/bin/env python3
"""
Enhance the changelog after semantic-release.
This script can be customized to add extra formatting or content to CHANGELOG.md.
"""

import os


def enhance_changelog():
    changelog_path = "CHANGELOG.md"
    if os.path.exists(changelog_path):
        with open(changelog_path, "r") as f:
            content = f.read()
        # Example: Add a note at the top
        enhanced_content = "# Changelog\n\n*Enhanced by script*\n\n" + content
        with open(changelog_path, "w") as f:
            f.write(enhanced_content)
        print("Changelog enhanced.")
    else:
        print("CHANGELOG.md not found.")


if __name__ == "__main__":
    enhance_changelog()
