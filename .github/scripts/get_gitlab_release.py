#!/usr/bin/env python3
"""Get latest GitLab release tag.

Usage: get_gitlab_release.py

Returns: tag name on stdout (e.g., v1.0.7)
"""

import json
import sys
import urllib.request


def main():
    url = "https://gitlab.com/mamie_ia/tracks-to-pictures/-/releases?per_page=1&order_by=created_at"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as r:
            releases = json.loads(r.read().decode())
        
        if releases:
            print(releases[0]['tag'])
        else:
            print('v1.0.0')
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        print('v1.0.0')


if __name__ == "__main__":
    main()
