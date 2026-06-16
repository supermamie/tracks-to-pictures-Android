#!/usr/bin/env python3
"""Fix web content structure in Android assets directory.

Handles 3 cases:
1. index.html at root → done
2. index.html in subfolder → move to root
3. Single folder at root → extract its contents to root
"""

import os
import sys
import re

def find_index_html(directory):
    """Find index.html recursively."""
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f == 'index.html':
                return os.path.join(root, f)
    return None

def get_root_subdirs(directory):
    """Get immediate subdirectories (not files)."""
    entries = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            entries.append(item)
    return entries

def fix_relative_links(directory):
    """Fix relative links in HTML files."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.html') or f.endswith('.htm'):
                html_files.append(os.path.join(root, f))
    
    for html_path in html_files:
        with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Fix ../css/ → css/ and ./js/ → js/
        # etc
        content = re.sub(r'\.\./([a-zA-Z0-9_-]+/)', r'\1', content)
        content = re.sub(r'\./([a-zA-Z0-9_-]+/)', r'\1', content)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    if len(sys.argv) < 2:
        print("Usage: fix_web_structure.py <web_directory>")
        sys.exit(1)
    
    web_dir = sys.argv[1]
    print(f"Checking web content in {web_dir}...")
    
    index = find_index_html(web_dir)
    
    if index and os.path.dirname(index) == web_dir:
        print("✅ index.html already at root")
        return
    
    root_dirs = get_root_subdirs(web_dir)
    
    if len(root_dirs) == 1:
        # Case: single folder at root (e.g., tracks-to-pictures-v1.0.3/)
        single = root_dirs[0]
        print(f"📁 Found single folder: {single}/")
        
        # Move everything from folder to root
        src = os.path.join(web_dir, single)
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(web_dir, item)
            
            if os.path.isdir(src_path):
                # Merge subdirectories
                import shutil
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.move(src_path, dst_path)
            else:
                if os.path.exists(dst_path):
                    os.remove(dst_path)
                os.rename(src_path, dst_path)
        
        print(f"✅ Moved contents of {single}/ to root")
    
    elif index:
        # Case: index.html in a subfolder (maybe nested)
        print(f"📄 Found index.html at: {index}")
        
        # Move to root
        os.rename(index, os.path.join(web_dir, 'index.html'))
        print(f"✅ Moved index.html to root")
    
    # Fix relative links
    print("🔧 Fixing relative links...")
    fix_relative_links(web_dir)
    
    print("✅ Done")

if __name__ == '__main__':
    main()
