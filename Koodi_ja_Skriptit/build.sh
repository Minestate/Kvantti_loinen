#!/bin/bash
echo "=== PERUSTA: THIN AIR KEYBOARD - LOPULLINEN VIIMEISTELY ==="

# 1. Puhdistus
rm -rf build classes.dex thinair.apk thinair.unaligned.apk
mkdir -p build/obj res/xml

# 2. Luodaan yhteensopiva mekaaninen manifesti (Target SDK 33 = Android 13/14 suorituskyky)
cat <<EOF > AndroidManifest.xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.perusta.thinair"
    android:versionCode="1"
    android:versionName="1.5">

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="33" />

    <application android:label="Thin Air Keyboard" android:hasCode="true">
        <service android:name=".PerustaKeyboardService"
                 android:permission="android.permission.BIND_INPUT_METHOD"
                 android:exported="true">
            <intent-filter>
                <action android:name="android.view.InputMethod" />
            </intent-filter>
            <meta-data android:name="android.view.im" android:resource="@xml/method.xml" />
        </service>
    </application>
</manifest>
EOF

# 3. Luodaan rajapintamääritys
cat <<EOF > res/xml/method.xml
<?xml version="1.0" encoding="utf-8"?>
<input-method xmlns:android="http://schemas.android.com/apk/res/android" />
EOF

# 4. Käännetään Java-rauta Java 8 -yhteensopivaksi
echo "[*] Käännetään Javan tavukoodi..."
javac -source 8 -target 8 -classpath ./android.jar -d build/obj PerustaKeyboardService.java

# 5. Muunnetaan classes.dexiksi
echo "[*] Muunnetaan rautakoodi dex-muotoon..."
dx --dex --output=classes.dex build/obj/

# 6. Pakataan ainekset suoralla mekaanisella varmuudella ilman haamunollia
echo "[*] Pakataan APK..."
zip -j thinair.unaligned.apk classes.dex
zip -r thinair.unaligned.apk AndroidManifest.xml res/

# 7. Allekirjoitus
echo "[*] Allekirjoitetaan paketti..."
if [ ! -f "perusta.keystore" ]; then
    keytool -genkey -v -keystore perusta.keystore -alias perusta -keyalg RSA -keysize 2048 -validity 10000 -storepass perustasalasana -keypass perustasalasana -dname "CN=Perusta, O=Tehdas, C=FI"
fi

apksigner sign --ks perusta.keystore --ks-pass pass:perustasalasana --out thinair.apk thinair.unaligned.apk

echo "=== VIIMEISTELY VALMIS ==="
ls -lh thinair.apk

#!/bin/bash

# Asetukset
VERSION="v1.0"
OUTPUT_FILE="Perusta_OS_${VERSION}.zip"

echo "[BUILD] Aloitetaan Perustan paketointi..."

# Tarkistetaan että vaadittavat tiedostot löytyvät
if [ ! -d "META-INF" ] || [ ! -f "module.prop" ]; then
    echo "[VIRHE] Projektin rakenne puutteellinen. Tarkista META-INF ja module.prop."
    exit 1
fi

# Poistetaan mahdollinen vanha paketti
if [ -f "$OUTPUT_FILE" ]; then
    rm "$OUTPUT_FILE"
fi

# Paketoidaan tiedostot .zip-muotoon
# -r = rekursiivinen, -q = hiljainen tila
zip -rq "$OUTPUT_FILE" META-INF system module.prop

if [ $? -eq 0 ]; then
    echo "[VALMIS] Paketti luotu: $OUTPUT_FILE"
    echo "[INFO] Voit nyt ladata tämän tiedoston GitHub Releases -sivulle."
else
    echo "[VIRHE] Paketointi epäonnistui."
    exit 1
fi
