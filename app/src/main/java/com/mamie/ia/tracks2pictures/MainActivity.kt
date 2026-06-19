package com.mamie.ia.tracks2pictures

import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
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
        val settings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.setGeolocationEnabled(true)
        settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW

        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView, request: WebResourceRequest
            ): WebResourceResponse? {
                val url = request.url.toString()
                if (!url.startsWith("file:///android_asset/")) return null

                val assetPath = url.substring("file:///android_asset/".length)
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

                return try {
                    val stream: InputStream = assets.open(assetPath)
                    WebResourceResponse(mimeType, "UTF-8", stream)
                } catch (e: IOException) {
                    null
                }
            }
        }

        webView.loadUrl("file:///android_asset/web/index.html")
    }
}
