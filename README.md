# Tracks to Pictures — Android

A generic Android WebView app that wraps any static website. No HTML or JS modifications required — the app intercepts all asset requests and serves them from bundled assets.

## Features

- **Generic** — Loads any static site without code changes
- **Offline mode** — Bundles web content inside APK (no network needed)
- **Geolocation** — Supports device GPS for map positioning
- **Error page** — Shows friendly error if web content is missing
- **Auto-versioning** — Version auto-determined from git releases (GitHub/GitLab)
- **Translation embedding** — Languages embedded automatically via `translations.js`
- **WebViewClient interceptor** — Serves assets from `file:///android_asset/` without CORS

## Architecture

```
app/src/main/assets/web/          ← Bundled web content
├── index.html                    ← Site root (no modifications needed)
├── js/app.js                     ← Site JS
├── css/style.css                 ← Site CSS
├── lib/leaflet.js                ← Site libs
├── translations.js               ← Auto-generated translations
└── ...
```

The app loads `file:///android_asset/web/index.html` and uses a `WebViewClient` to intercept all requests and serve files from `assets/`.

## Build

### Manual build (GitHub Actions)

1. Go to **Actions** tab
2. Click **Build APK**
3. Click **Run workflow**
4. Wait for build to complete
5. Download APK from **Artifacts**

### Workflow steps

The CI/CD pipeline runs these steps:

1. **Checkout** — Clone Android repo
2. **Download web archive** — Fetch from Git repo (GitHub/GitLab/direct URL)
3. **Fix web structure** — Move `index.html` to root if nested
4. **Copy assets** — Copy web content to `app/src/main/assets/web/`
5. **Build version** — Increment from existing Android releases
6. **Build APK** — Gradle `assembleRelease`
7. **Create release** — GitHub release with APK + assets

### Configuration

All configuration comes from `app-release-metadata.yml`:

| Field | Purpose | Example |
|-------|---------|---------|
| `git_repo` | Git repo for content bundling | `https://gitlab.com/mamie_ia/tracks-to-pictures` |
| `archive_url` | Direct URL to download | `https://example.com/web-archive.zip` |
| `web_url_fallback` | WebView fallback URL | `""` (empty = error page) |

### Forking for a new site

To adapt this app for another static site:

1. **Fork** the Android repo
2. **Edit** `app-release-metadata.yml` — change `git_repo` or `archive_url`
3. **Launch** the workflow — it adapts automatically

The app works with any static site — no HTML, CSS, or JS modifications required.

## Contributing

Report issues on [GitLab Issues](https://gitlab.com/mamie_ia/tracks-to-pictures/-/issues).

## License

GPL-3.0-or-later
