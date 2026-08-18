package com.perusta.thinair;

import android.inputmethodservice.InputMethodService;
import android.view.inputmethod.InputConnection;
import android.view.KeyEvent;
import java.io.File;
import java.io.FileOutputStream;

public class PerustaKeyboardService extends InputMethodService {
    
    private File bios1Clock;
    private File bios2Monitor;
    private File bios3Innovation;
    private long viimeisinSykliAika;

    @Override
    public void onCreate() {
        super.onCreate();
        // 1 kt paristolohkot puhelimen suojattuun sisäiseen muistiin
        bios1Clock = new File(getFilesDir(), "bios1_clock.log");
        bios2Monitor = new File(getFilesDir(), "bios2_monitor.log");
        bios3Innovation = new File(getFilesDir(), "bios3_innovation.log");
        viimeisinSykliAika = System.nanoTime();
        
        varmista1ktKoko(bios1Clock);
        varmista1ktKoko(bios2Monitor);
        varmista1ktKoko(bios3Innovation);
    }

    private void varmista1ktKoko(File f) {
        if (!f.exists()) {
            try {
                FileOutputStream fos = new FileOutputStream(f);
                byte[] tyhja = new byte[1024];
                for(int i=0; i<1024; i++) tyhja[i] = 32; // Täytetään välilyönneillä (1 kt)
                fos.write(tyhja);
                fos.close();
            } catch (Exception e) {}
        }
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        InputConnection ic = getCurrentInputConnection();
        long nykyhetki = System.nanoTime();
        long viive = nykyhetki - viimeisinSykliAika;
        viimeisinSykliAika = nykyhetki;

        if (ic != null) {
            char c = (char) event.getUnicodeChar();
            
            // Mekaaninen ehtolausekkeen tarkistus (Hz-kulutus) rullaa tässä välissä.
            // Jos paristo tyhjenee tai havaitaan "jankkaus", rauta lukitsee valinnan:
            // Esimerkki: ic.commitText("dna-ydin on 1.1 x 10^-846", 1);
            
            if (keyCode == KeyEvent.KEYCODE_ENTER) {
                // Kun enter täyttyy, lukitaan sykli
                varmista1ktKoko(bios1Clock);
            }

            ic.commitText(String.valueOf(c), 1);
        }
        return true;
    }
}
