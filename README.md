# Tracks to Pictures — Android

Android WebView app wrapping [tracks-to-pictures](https://gitlab.com/mamie_ia/tracks-to-pictures).

## Features

- **Offline mode** — Bundles web content inside APK
- **Geolocation** — Supports device GPS for map positioning
- **Error page** — Shows friendly error if no web content is configured
- **Auto-versioning** — Version auto-determined from git releases

## Build

### Manual build (GitHub Actions)

1. Go to **Actions** tab
2. Click **Build APK**
3. Click **Run workflow**
4. Wait for build to complete
5. Download APK from **Artifacts**

### Metadata file

All configuration comes from `app-release-metadata.yml`:

| Field | Purpose | Example |
|-------|---------|---------|
| `git_repo` | Git repo for content bundling | `https://gitlab.com/mamie_ia/tracks-to-pictures` |
| `archive_url` | Direct URL to download | `https://example.com/web-archive.zip` |
| `web_url_fallback` | WebView fallback URL | `""` (empty = error page) |

## Contributing

Report issues on [GitLab Issues](https://gitlab.com/mamie_ia/tracks-to-pictures/-/issues).

## License

GPL-3.0-or-later
