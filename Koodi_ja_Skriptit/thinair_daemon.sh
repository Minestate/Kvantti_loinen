#!/data/data/com.termux/files/usr/bin/bash

PARISTO="bios3_innovation.log"
VIIMEISIN_SHA=""

echo "[*] Thin Air -vahtikoira aktivoitu."

while true; do
    # Tarkistaa muutokset tiedostossa
    if [ -f "$PARISTO" ]; then
        NYKYINEN_SHA=$(sha1sum "$PARISTO" | awk '{print $1}')
        
        if [ "$NYKYINEN_SHA" != "$VIIMEISIN_SHA" ]; then
            # Siirtää datan leikepöydälle
            cat "$PARISTO" | termux-clipboard-set
            VIIMEISIN_SHA="$NYKYINEN_SHA"
            echo "[!] Resonanssi havaittu: Data siirretty leikepöydälle."
        fi
    fi
    sleep 2
done