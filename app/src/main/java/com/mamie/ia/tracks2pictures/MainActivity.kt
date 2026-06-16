package com.mamie.ia.tracks2pictures

import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import java.io.IOException
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
        
        // WebViewClient: intercepts all requests and serves from assets/
        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView, request: WebResourceRequest
            ): WebResourceResponse? {
                val url = request.url.toString()
                
                // Only intercept file:///android_asset/ URLs (local assets)
                if (!url.startsWith("file:///android_asset/")) {
                    return null
                }
                
                // Get the relative path from the URL
                val assetPath = url.substring("file:///android_asset/".length)
                
                // Serve the file
                return try {
                    val mimeType = when {
                        assetPath.endsWith(".html") || assetPath.endsWith(".htm") -> "text/html; charset=utf-8"
                        assetPath.endsWith(".css") -> "text/css; charset=utf-8"
                        assetPath.endsWith(".js") -> "application/javascript; charset=utf-8"
                        assetPath.endsWith(".json") -> "application/json; charset=utf-8"
                        assetPath.endsWith(".svg") -> "image/svg+xml"
                        assetPath.endsWith(".png") -> "image/png"
                        assetPath.endsWith(".jpg") || assetPath.endsWith(".jpeg") -> "image/jpeg"
                        assetPath.endsWith(".gif") -> "image/gif"
                        assetPath.endsWith(".woff") || assetPath.endsWith(".woff2") -> "font/woff"
                        assetPath.endsWith(".ttf") -> "font/ttf"
                        else -> "application/octet-stream"
                    }
                    
                    val stream: InputStream = assets.open(assetPath)
                    WebResourceResponse(mimeType, "UTF-8", stream)
                } catch (e: IOException) {
                    null
                }
            }
        }
        
        // Load index.html from assets
        webView.loadUrl("file:///android_asset/web/index.html")
    }
}
