#!/data/data/com.termux/files/usr/bin/bash

# Asetetaan paristotiedoston polku
PARISTO="bios3_innovation.log"
VIIMEISIN_SHA=""

echo "[*] Thin Air -vahtikoira käynnistetty..."
echo "[*] Tarkkaillaan 1kt paristoa: $PARISTO"

while true; do
    # Lasketaan tiedoston sisältö (SHA1-summa) muutosten havaitsemiseksi
    NYKYINEN_SHA=$(sha1sum "$PARISTO" | awk '{print $1}')
    
    if [ "$NYKYINEN_SHA" != "$VIIMEISIN_SHA" ]; then
        # Päivitetään leikepöytä
        cat "$PARISTO" | tr -d '\0' | termux-clipboard-set
        VIIMEISIN_SHA="$NYKYINEN_SHA"
        echo "[!] Paristo päivitetty leikepöydälle."
    fi
    
    # Lepotila syklin välissä
    sleep 2
done
