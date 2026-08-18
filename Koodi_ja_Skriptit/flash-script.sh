# Asennusskripti
cp /data/adb/modules/perusta/bin/perusta_kaynnistin.sh /system/bin/perusta
chmod +x /system/bin/perusta
# Käynnistetään daemon
/system/bin/perusta --start
