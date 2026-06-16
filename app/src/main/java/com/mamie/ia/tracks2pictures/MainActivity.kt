package com.mamie.ia.tracks2pictures

import android.os.Bundle
import android.util.Log
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import java.io.InputStream

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        val webView = findViewById<WebView>(R.id.webview)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.setGeolocationEnabled(true)
        webView.settings.mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        
        // Serve translation JSON files directly from assets (bypasses CORS for file:/// mode)
        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView, request: WebResourceRequest
            ): WebResourceResponse? {
                val url = request.url.toString()
                if (url.contains("/android_asset/web/js/translations.")) {
                    val assetPath = url.replace("file:///android_asset/", "")
                    try {
                        val stream: InputStream = assets.open(assetPath)
                        val mime = "application/json"
                        return WebResourceResponse(mime, "UTF-8", stream)
                    } catch (e: Exception) {
                        Log.w("MainActivity", "Failed to serve $assetPath: ${e.message}")
                    }
                }
                return null
            }
        }
        
        // Try to load local bundle first (for offline use)
        val localUrl = "file:///android_asset/web/index.html"
        if (tryLoadAsset("web/index.html")) {
            webView.loadUrl(localUrl)
            Log.i("MainActivity", "Loading local: $localUrl")
        } else {
            if (BuildConfig.WEB_URL == "about:blank") {
                webView.loadUrl("file:///android_asset/error.html")
                Log.w("MainActivity", "No web URL configured, loading error page")
            } else {
                webView.loadUrl(BuildConfig.WEB_URL)
                Log.w("MainActivity", "Loading remote: ${BuildConfig.WEB_URL}")
            }
        }
    }
    
    private fun tryLoadAsset(assetPath: String): Boolean {
        return try {
            assets.open(assetPath).close()
            true
        } catch (e: Exception) {
            Log.e("MainActivity", "Asset not found: $assetPath")
            false
        }
    }
}
