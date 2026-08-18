#!/bin/bash
# 1. Pysäytetään mahdolliset vanhat palvelimet
pkill -f "python3 -m http.server"

# 2. Käynnistetään palvelin taustalle (portti 8080)
# Luodaan väliaikainen hakemisto dashboardia varten jos tarpeen
python3 -m http.server 8080 > /dev/null 2>&1 &

# 3. Odotetaan reaktoria
sleep 2

# 4. Avataan selain
termux-open "http://127.0.0.1:8080"
