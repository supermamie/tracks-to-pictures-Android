#!/usr/bin/env python3
"""Place extracted web archive into assets/web/.

Rules:
1. If index.html is at root level -> copy everything
2. If index.html is in a single folder -> copy that folder
3. Otherwise -> build error

Usage: place_web_content.py <build_dir> <assets_dir>
"""

import os
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: place_web_content.py <build_dir> <assets_dir>", file=sys.stderr)
        sys.exit(1)

    build_dir = sys.argv[1]
    assets_dir = sys.argv[2]

    # Find index.html
    index_path = None
    for root, dirs, files in os.walk(build_dir):
        if "index.html" in files:
            index_path = os.path.join(root, "index.html")
            break

    if not index_path:
        print("ERROR: No index.html found in web archive", file=sys.stderr)
        sys.exit(1)

    # Determine where index.html is located
    index_dir = os.path.dirname(index_path)

    # Check if index.html is at the root of the extracted archive
    # (one level below build_dir, ignoring the extracted folder name)
    root_candidates = []
    for item in os.listdir(build_dir):
        item_path = os.path.join(build_dir, item)
        if os.path.isdir(item_path):
            root_candidates.append(item)

    # Check if index.html is directly under build_dir (root level)
    index_is_root = False
    if os.path.exists(os.path.join(build_dir, "index.html")):
        index_is_root = True

    # If not root, check if there's exactly one folder containing index.html
    index_folder = None
    for candidate in root_candidates:
        candidate_index = os.path.join(build_dir, candidate, "index.html")
        if os.path.exists(candidate_index):
            if index_folder is None:
                index_folder = candidate  # Found first folder
            else:
                print("ERROR: index.html found in multiple folders", file=sys.stderr)
                sys.exit(1)

    # Determine source folder to copy
    if index_is_root:
        # index.html at root -> copy everything from build_dir
        src = build_dir
    elif index_folder:
        # index.html in exactly one folder -> copy that folder's content
        src = os.path.join(build_dir, index_folder)
    else:
        print("ERROR: index.html not found at root or in a single folder", file=sys.stderr)
        sys.exit(1)

    print(f"Source: {src}")

    # Create destination
    os.makedirs(assets_dir, exist_ok=True)

    # Copy all files from src to assets_dir
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(assets_dir, item)

        if os.path.isdir(src_path):
            import shutil
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
        else:
            import shutil
            shutil.copy2(src_path, dst_path)

    print(f"Contents placed in {assets_dir}:")
    for item in os.listdir(assets_dir):
        print(f"  {item}")


if __name__ == "__main__":
    main()
