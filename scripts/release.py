#!/usr/bin/env python3
"""Release helper: validate CHANGELOG, create release commit, push, and open PR.

Usage:
    python scripts/release.py <version>
    e.g. python scripts/release.py 0.2.0
"""

from __future__ import annotations

import re
import subprocess
import sys


def run(cmd: str, *, check: bool = True) -> str:
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, check=check
    )
    return result.stdout.strip()


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <version>")
        sys.exit(1)

    version = sys.argv[1]
    tag = f"v{version}"

    # Validate version format
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        print(f"Error: invalid version format: {version}")
        sys.exit(1)

    # Check CHANGELOG.md has entry for this version
    with open("CHANGELOG.md") as f:
        changelog = f.read()

    if f"## [{version}]" not in changelog:
        print(f"Error: CHANGELOG.md missing entry for ## [{version}]")
        sys.exit(1)

    # Check we're on develop
    branch = run("git branch --show-current")
    if branch != "develop":
        print(f"Error: must be on develop branch (currently on {branch})")
        sys.exit(1)

    # Check working tree is clean
    status = run("git status --porcelain")
    if status:
        print("Error: working tree is not clean")
        sys.exit(1)

    # Check tag doesn't exist
    existing_tags = run("git tag -l")
    if tag in existing_tags.split("\n"):
        print(f"Error: tag {tag} already exists")
        sys.exit(1)

    # Push develop
    print("Pushing develop...")
    run("git push origin develop")

    # Create PR to main
    print("Creating release PR...")
    pr_url = run(
        f"gh pr create --base main --head develop "
        f'--title "release: {tag}" '
        f'--body "Release {tag}\\n\\nSee CHANGELOG.md for details."'
    )
    print(f"Release PR created: {pr_url}")
    print("\nNext steps:")
    print("  1. Review and merge the PR (squash merge)")
    print(f"  2. auto-release.yml will create tag {tag} and GitHub Release")
    print("  3. release.yml will publish to TestPyPI then PyPI")


if __name__ == "__main__":
    main()
