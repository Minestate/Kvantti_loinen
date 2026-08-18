# quantum_bot_v1.py - Ydinlogiikka
import os
import sys

# Injektiopiste: Botti tarkistaa, onko lisäyksiä olemassa
if os.path.exists("modifications.py"):
    import modifications
    modifications.apply_logic(self) # Botti kutsuu muokattua logiikkaa