# Tracks to Pictures — Android

Application Android WebView enrobant [tracks-to-pictures](https://gitlab.com/mamie_ia/tracks-to-pictures).

## Construction

### Build manuel (GitHub Actions)

1. Aller dans l'onglet **Actions** du repo
2. Cliquer sur **Build APK** → **Run workflow**
3. Configurer les paramètres (version name, URL du web app)
4. Cliquer **Run**

L'APK signé est automatiquement uploadé en tant que draft sur GitHub Releases.

### Build local

```bash
./gradlew assembleRelease
```

L'APK signé se trouve dans `app/build/outputs/apk/release/`.

## Signature

Le keystore public est `app/release-key.keystore` :

- **Alias :** `trackstopictures`
- **Passwords :** `android` (store + key)
- **Validité :** 10 000 jours

## Déploiement

- **F-Droid :** le build est reproductible (signature copiée du keystore public)
- **Distribution directe :** l'APK signé est disponible sur GitHub Releases
