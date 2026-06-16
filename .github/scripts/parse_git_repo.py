#!/usr/bin/env python3
"""Parse git_repo URL from app-release-metadata.yml or site-config.json.

Returns:
  (platform, repo_path) where platform is "github", "gitlab", or "generic"
  repo_path is the path without protocol (e.g., "mamie_ia/tracks-to-pictures")
"""

import json
import sys
import re


def parse_url(url):
    """Extract platform and repo path from a URL."""
    if not url or "://" not in url:
        return "generic", url
    
    platform = url.split("://")[1]
    
    if platform.startswith("github.com"):
        repo = platform.split("github.com/")[-1].replace(".git", "").rstrip("/")
        return "github", repo
    elif platform.startswith("gitlab.com"):
        repo = platform.split("gitlab.com/")[-1].replace(".git", "").rstrip("/")
        return "gitlab", repo
    elif platform.startswith("git."):
        return "generic", platform
    else:
        return "generic", platform


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_git_repo.py <metadata.yml> [config.json]")
        sys.exit(1)
    
    metadata_path = sys.argv[1]
    config_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Try app-release-metadata.yml first
    git_repo = None
    try:
        with open(metadata_path, 'r') as f:
            content = f.read()
        for line in content.split('\n'):
            if line.strip().startswith('git_repo:'):
                # Extract value between quotes or after colon
                value = line.split(':', 1)[1].strip()
                git_repo = value.strip('" ').strip("' ")
                if git_repo:
                    break
    except Exception as e:
        print(f"⚠️ Could not read {metadata_path}: {e}")
    
    # Fallback to site-config.json
    if not git_repo and config_path:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            source = config.get('source', '')
            if isinstance(source, str):
                git_repo = source
            elif isinstance(source, dict):
                if source.get('host') and source.get('repo'):
                    git_repo = f"https://{source['host']}/{source['repo']}"
        except Exception as e:
            print(f"⚠️ Could not read {config_path}: {e}")
    
    if not git_repo:
        print("❌ No git_repo found in metadata or config")
        sys.exit(1)
    
    platform, repo = parse_url(git_repo)
    print(f"platform={platform}")
    print(f"repo={repo}")
    print(f"git_repo={git_repo}")


if __name__ == '__main__':
    main()
