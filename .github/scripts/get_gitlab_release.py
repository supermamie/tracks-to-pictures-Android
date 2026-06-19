#!/usr/bin/env python3
"""Get latest GitLab release tag via git ls-remote.

Returns: tag name on stdout (e.g., v1.0.7)
"""

import os
import sys
import subprocess


def main():
    repo_url = "https://gitlab.com/mamie_ia/tracks-to-pictures.git"
    
    try:
        # Use git ls-remote to list all tags (only regular tags, not annotated)
        result = subprocess.run(
            ["git", "ls-remote", "--tags", "--sort=-version:refname", repo_url],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            # First line is the latest tag
            lines = result.stdout.strip().split("\n")
            if lines:
                # Format: <hash>\trefs/tags/<tag>
                parts = lines[0].split("\t")
                if len(parts) >= 2:
                    tag = parts[1].replace("refs/tags/", "").replace("^{}", "")
                    print(tag)
                    return
        
        print("v1.0.0")
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        print("v1.0.0")


if __name__ == "__main__":
    main()
