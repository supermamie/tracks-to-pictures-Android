#!/usr/bin/env python3
"""Get latest release tag and compute next version.

Usage: get_version.py <owner> <name> <gh_token>

Returns: version string on stdout (e.g., v1.0.7.2)
"""

import json
import sys
import re


def main():
    if len(sys.argv) != 4:
        print("Usage: get_version.py <owner> <name> <token>", file=sys.stderr)
        sys.exit(1)

    owner, name, token = sys.argv[1], sys.argv[2], sys.argv[3]
    url = f"https://api.github.com/repos/{owner}/{name}/releases"

    try:
        import urllib.request
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"token {token}")
        with urllib.request.urlopen(req) as r:
            releases = json.loads(r.read().decode())
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        print("v0.0.1")
        return

    if not releases:
        print("v0.0.1")
        return

    # Parse versions: strip 'v', split by '.', convert to numeric tuples
    versions = []
    for rel in releases:
        tag = rel.get("tag_name", "")
        if not tag:
            continue
        # Remove 'v' prefix
        num = re.sub(r"^v", "", tag, flags=re.IGNORECASE)
        parts = num.split(".")
        nums = []
        for p in parts:
            try:
                nums.append(int(p))
            except ValueError:
                nums.append(0)
        versions.append((nums, tag))

    if not versions:
        print("v0.0.1")
        return

    # Sort numerically
    versions.sort(key=lambda x: x[0])
    latest_tag = versions[-1][1]

    # Increment last segment
    num = re.sub(r"^v", "", latest_tag, flags=re.IGNORECASE)
    parts = num.split(".")
    try:
        parts[-1] = str(int(parts[-1]) + 1)
    except ValueError:
        parts[-1] = "1"

    new_tag = "v" + ".".join(parts)
    print(new_tag)


if __name__ == "__main__":
    main()
