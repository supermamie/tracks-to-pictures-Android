#!/usr/bin/env python3
"""Modify app/build.gradle to set version and WEB_URL fields.

Usage:
    python3 modify_build_gradle.py <version_name> <version_code> <web_url>

Where:
    version_name: string (e.g., "1.0.1")
    version_code: integer (e.g., 1001)
    web_url: string or "about:blank"
"""

import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 modify_build_gradle.py <version_name> <version_code> <web_url>", file=sys.stderr)
        sys.exit(1)

    version_name = sys.argv[1]
    version_code = sys.argv[2]
    web_url = sys.argv[3]
    gradle_file = "app/build.gradle"

    # Build the escaped WEB_URL value for Gradle
    # In Gradle (Groovy), we need: \" about:blink " (backslash-quote inside the string)
    # Using chr() to avoid any escaping confusion
    bs = chr(92)    # backslash
    q = chr(34)     # double quote

    if web_url == "about:blank":
        escaped_web_url = bs + q + "about:blank" + bs + q
    else:
        escaped_web_url = bs + q + web_url + bs + q

    with open(gradle_file, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if "versionName" in line:
            new_lines.append(f'versionName "{version_name}"\n')
        elif "versionCode" in line:
            new_lines.append(f'versionCode {version_code}\n')
        elif "WEB_URL" in line:
            new_lines.append(f'buildConfigField "String", "WEB_URL", "{escaped_web_url}"\n')
        else:
            new_lines.append(line)

    with open(gradle_file, "w") as f:
        f.writelines(new_lines)

    print(f"✅ Updated: versionName={version_name}, versionCode={version_code}, WEB_URL={web_url}")

if __name__ == "__main__":
    main()
