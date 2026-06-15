# Tracks to Pictures — Android

Android WebView app wrapping [tracks-to-pictures](https://gitlab.com/mamie_ia/tracks-to-pictures).

## Build

### Manual build (GitHub Actions)

1. Go to the **Actions** tab in the repo
2. Click **Build APK** → **Run workflow**
3. Configure parameters (version name, web URL)
4. Click **Run**

The signed APK is automatically uploaded as a draft to GitHub Releases.

### Local build

```bash
./gradlew assembleRelease
```

The signed APK is located in `app/build/outputs/apk/release/`.

## Signing

The public keystore is `app/release-key.keystore`:

- **Alias:** `trackstopictures`
- **Passwords:** `android` (store + key)
- **Validity:** 10,000 days

## Deployment

- **F-Droid:** reproducible build (signature copied from public keystore)
- **Direct distribution:** the signed APK is available on GitHub Releases
