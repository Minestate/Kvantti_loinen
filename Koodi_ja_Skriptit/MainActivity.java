import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class PerustaBrowser extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        WebView browser = new WebView(this);
        browser.getSettings().setJavaScriptEnabled(true);
        browser.setWebViewClient(new WebViewClient());
        browser.loadUrl("https://perusta.local"); // Tai paikallinen reaktori
        setContentView(browser);
    }
}
