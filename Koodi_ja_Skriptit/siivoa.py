import os
import shutil

class KvanttiNäkymätönMoottori:
    def __init__(self, kohde_asema="F"):
        self.asema = f"{kohde_asema.upper()}:\\"

        # TIUKAT PÄÄKATEGORIAT (Ainoat kansiot, jotka jäävät näkyviin)
        self.FORMAATIT = {
            "Dokumentit": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".txt", ".csv", ".rtf", ".odt", ".md"],
            "Kuvat_ja_Grafiikka": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp", ".psd"],
            "Media_Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "Media_Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"],
            "Arkistot_ja_Paketit": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".apk", ".jar", ".msi"],
            "Koodi_ja_Skriptit": [".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".sql", ".sh", ".ps1", ".bat", ".cmd", ".cs", ".cpp", ".c", ".yml"],
            "Ohjelmat_ja_Suoritettavat": [".exe", ".bin", ".msi"],
            "Jarjestelma_ja_Asetukset": [".sys", ".dll", ".dat", ".db", ".log", ".ini", ".cfg", ".config"],
            "Pelit_ja_Data": [".vdf", ".wld", ".map", ".bak", ".ess", ".sav"]
        }

    def _hae_kategoria(self, tiedosto):
        paate = os.path.splitext(tiedosto)[1].lower()
        if not paate:
            return "Ilman_Paatetta"
        for luokka, paatteet in self.FORMAATIT.items():
            if paate in paatteet:
                return luokka
        return "Järjestelmä_ja_Sekalaiset"

    def suorita_näkymätön_siivous(self):
        if not os.path.exists(self.asema):
            print(f"❌ Asemaa {self.asema} ei löydy.")
            return

        sallitut_kansiot = set(self.FORMAATIT.keys())
        sallitut_kansiot.update(["Ilman_Paatetta", "Järjestelmä_ja_Sekalaiset", "System Volume Information", "$RECYCLE.BIN"])

        siirretty = 0

        for root, dirs, files in os.walk(self.asema, topdown=False):
            suhteellinen = os.path.relpath(root, self.asema)
            paakansio = suhteellinen.split(os.sep)[0] if suhteellinen != "." else ""

            # Ei kosketa jo järjestettyihin pääkansioihin
            if paakansio in sallitut_kansiot:
                continue

            for file in files:
                if file.startswith("$") or file.endswith(".tmp"):
                    continue

                lahde = os.path.join(root, file)
                kohde_kategoria = self._hae_kategoria(file)
                kohde_dir = os.path.join(self.asema, kohde_kategoria)
                os.makedirs(kohde_dir, exist_ok=True)

                kohde = os.path.join(kohde_dir, file)
                
                # Törmäyksenesto
                if os.path.exists(kohde) and lahde != kohde:
                    nimi, paate = os.path.splitext(file)
                    kohde = os.path.join(kohde_dir, f"{nimi}_uusi{paate}")

                try:
                    shutil.move(lahde, kohde)
                    siirretty += 1
                except Exception:
                    pass

            # Poistetaan tyhjät vanhat kansiot
            if root != self.asema:
                try:
                    if not os.listdir(root):
                        os.rmdir(root)
                except Exception:
                    pass

        print(f"✔ Valmis! Kädenjälki asetettu aseman {self.asema} kansiorakenteeseen ({siirretty} tiedostoa järjestetty).")

if __name__ == "__main__":
    # Ajetaan suoraan taustalla kohdeasemalle F:
    moottori = KvanttiNäkymätönMoottori(kohde_asema="F")
    moottori.suorita_näkymätön_siivous()