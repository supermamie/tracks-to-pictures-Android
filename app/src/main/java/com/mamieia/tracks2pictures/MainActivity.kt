package com.mamieia.tracks2pictures

import android.os.Bundle
import android.util.Log
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        val webView = findViewById<WebView>(R.id.webview)
        webView.settings.javaScriptEnabled = true
        webView.webViewClient = WebViewClient()
        webView.settings.domStorageEnabled = true
        webView.settings.setGeolocationEnabled(true)
        webView.settings.mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        
        // Try to load local bundle first (for offline use)
        val localUrl = "file:///android_asset/web/index.html"
        if (tryLoadAsset(webView, "web/index.html")) {
            webView.loadUrl(localUrl)
        } else {
            // Fallback to remote URL or local error page
            if (BuildConfig.WEB_URL == "about:blank") {
                webView.loadUrl("file:///android_asset/error.html")
                Log.w("MainActivity", "No web URL configured, loading error page")
            } else {
                webView.loadUrl(BuildConfig.WEB_URL)
                Log.w("MainActivity", "No local bundle found, loading remote URL: ${BuildConfig.WEB_URL}")
            }
        }
    }
    
    private fun tryLoadAsset(webView: WebView, assetPath: String): Boolean {
        return try {
            val inputStream = assets.open(assetPath)
            inputStream.close()
            true
        } catch (e: Exception) {
            Log.e("MainActivity", "Failed to load asset: $assetPath", e)
            false
        }
    }
}
