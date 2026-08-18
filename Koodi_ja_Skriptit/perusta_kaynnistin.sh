#!/bin/bash
# PERUSTA - Järjestelmän käynnistysskripti

echo "[EMOLEVY] Herätetään perusta..."

# 1. Käynnistä nanoäly-skanneri taustalle
python3 perusta_ydin_skanneri.py & 

# 2. Käynnistä väylä (WebSocket/HTTP-silta)
python3 perusta_selain.py &

# 3. Isoälyn valvonta (valvoo parametrien funktioita)
python3 isoaly_linkki.py &

echo "[EMOLEVY] Järjestelmä operatiivinen."

# Esimerkki: Avaa selain heti kun Perusta käynnistyy
xdg-open http://localhost:8000

# Automaattinen käynnistys ilman näppäimistöä
# Nanoälyt tarkkailevat tiedostojärjestelmän muutoksia automaattisesti
nohup python3 perusta_ydin_skanneri.py > /dev/null 2>&1 &
nohup python3 ydin_silta.py > /dev/null 2>&1 &
