#!/usr/bin/env python3
"""Embed all translation JSON files into index.html at build time.

Reads translations from assets/web/js/translations.*.json
and injects a <script> tag into index.html before i18n.js.

Usage: python3 embed_translations.py <assets/web/>
"""

import json
import os
import sys
import glob
import re


def main():
    if len(sys.argv) < 2:
        print("Usage: embed_translations.py <web_assets_dir>")
        sys.exit(1)

    web_dir = sys.argv[1]
    js_dir = os.path.join(web_dir, 'js')
    index_html = os.path.join(web_dir, 'index.html')

    # Collect translations
    translations = {}
    for f in sorted(glob.glob(os.path.join(js_dir, 'translations.*.json'))):
        lang = os.path.basename(f).replace('translations.', '').replace('.json', '')
        with open(f, 'r', encoding='utf-8') as fh:
            translations[lang] = json.load(fh)

    if not translations:
        print("No translations found — skipping")
        return

    print(f"Embedded {len(translations)} translations into {index_html}")

    # Build the script content
    script = f'<script>\n'
    script += f'/* Embedded translations — loaded before i18n.js */\n'
    script += f'var i18n_raw = ' + json.dumps(translations, ensure_ascii=False) + ';\n'
    script += f'localStorage.setItem("tracks3_lang", "fr");\n'
    script += f'</script>\n'

    # Read index.html
    with open(index_html, 'r', encoding='utf-8') as f:
        html = f.read()

    # Inject before i18n.js script tag
    old = '  <script src="js/i18n.js"></script>'
    if old in html:
        html = html.replace(old, f'  {script}\n  <script src="js/i18n.js"></script>')
    else:
        # Try alternative format
        old = '<script src="js/i18n.js"></script>'
        if old in html:
            html = html.replace(old, f'{script}\n  <script src="js/i18n.js"></script>')
        else:
            print("Warning: i18n.js tag not found — appending before closing </body>")
            html = html.replace('</body>', f'  {script}\n  <script src="js/i18n.js"></script>\n</body>')

    with open(index_html, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    main()
