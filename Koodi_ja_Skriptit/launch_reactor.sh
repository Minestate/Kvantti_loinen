#!/bin/bash
# PERUSTA HQ: REAKTORIN KÄYNNISTYSJÄRJESTELMÄ

echo "[SYSTEM] DNA-tarkistus aloitettu..."
# Tarkistetaan DNA-yhteys ennen laukaisua
python3 -c "from core_dna import DNA_CORE, valtuuta_prosessi; exit(0 if valtuuta_prosessi(DNA_CORE) else 1)"
if [ $? -ne 0 ]; then
    echo "[CRITICAL] DNA-ydin ei vastaa. Laukaisu estetty."
    exit 1
fi

echo "[SYSTEM] Reaktori lämpenemässä..."

# 1. Käynnistetään tietokannan ylläpitäjä (Suodatin)
python3 suodatin_asema.py &

# 2. Käynnistetään analyysivalvoja
python3 analyysi_asema.py &

# 3. Aktivoi itse-duplikoituva botti
python3 quantum_bot.py &

echo "[SYSTEM] Reaktori aktivoitu. Autonomia saavutettu."
