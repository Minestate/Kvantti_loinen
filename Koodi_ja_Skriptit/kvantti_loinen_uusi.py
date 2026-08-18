import os
import json
import shutil
import argparse
from datetime import datetime

# VAKIOASETUKSET (Luodaan config.json jos sitä ei ole)
DEFAULT_CONFIG = {
    "FORMAATIT": {
        "Dokumentit": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".txt", ".csv", ".rtf", ".odt", ".md"],
        "Kuvat_ja_Grafiikka": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp", ".psd"],
        "Media_Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Media_Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"],
        "Arkistot_ja_Paketit": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".apk", ".jar", ".msi"],
        "Koodi_ja_Skriptit": [".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".sql", ".sh", ".ps1", ".bat", ".cs", ".cpp", ".yml"],
        "Ohjelmat_ja_Suoritettavat": [".exe", ".bin"],
        "Jarjestelma_ja_Asetukset": [".sys", ".dll", ".dat", ".db", ".log", ".ini", ".cfg"]
    },
    "OHITA_KANSIOT": ["System Volume Information", "$RECYCLE.BIN", ".git", "node_modules"]
}

class KvanttiLoinenGitHub:
    def __init__(self, asema="F", dry_run=False, config_file="config.json"):
        self.asema = f"{asema.upper()}:\\"
        self.dry_run = dry_run
        self.config = self._lataa_config(config_file)
        self.undo_loki = []

    def _lataa_config(self, tiedosto):
        if os.path.exists(tiedosto):
            with open(tiedosto, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(tiedosto, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
            return DEFAULT_CONFIG

    def _hae_kategoria(self, tiedosto):
        paate = os.path.splitext(tiedosto)[1].lower()
        if not paate:
            return "Ilman_Paatetta"
        for luokka, paatteet in self.config["FORMAATIT"].items():
            if paate in paatteet:
                return luokka
        return "Järjestelmä_ja_Sekalaiset"

    def suorita(self):
        tila = "[SIMULAATIO / DRY-RUN]" if self.dry_run else "[AITO SUORITUS]"
        print(f"⚡ Käynnistetään Kvantti_loinen {tila} kohteelle {self.asema}\n")

        sallitut = set(self.config["FORMAATIT"].keys())
        sallitut.update(["Ilman_Paatetta", "Järjestelmä_ja_Sekalaiset"])
        sallitut.update(self.config["OHITA_KANSIOT"])

        siirretty = 0

        for root, dirs, files in os.walk(self.asema, topdown=False):
            suhteellinen = os.path.relpath(root, self.asema)
            paakansio = suhteellinen.split(os.sep)[0] if suhteellinen != "." else ""

            if paakansio in sallitut:
                continue

            for file in files:
                if file.startswith("$") or file.endswith(".tmp"):
                    continue

                lahde = os.path.join(root, file)
                kategoria = self._hae_kategoria(file)
                kohde_dir = os.path.join(self.asema, kategoria)
                kohde = os.path.join(kohde_dir, file)

                if os.path.exists(kohde) and lahde != kohde:
                    nimi, paate = os.path.splitext(file)
                    kohde = os.path.join(kohde_dir, f"{nimi}_uusi{paate}")

                if self.dry_run:
                    print(f"  [Dry-Run] Siirrettäisiin: {file} -> {kategoria}/")
                else:
                    os.makedirs(kohde_dir, exist_ok=True)
                    try:
                        shutil.move(lahde, kohde)
                        self.undo_loki.append({"lahde": lahde, "kohde": kohde})
                        siirretty += 1
                    except Exception as e:
                        print(f"  [⚠️] Virhe: {e}")

            # Poistetaan tyhjät kumpareet (vain todellisessa ajossa)
            if not self.dry_run and root != self.asema:
                try:
                    if not os.listdir(root):
                        os.rmdir(root)
                except Exception:
                    pass

        if not self.dry_run:
            self._tallenna_undo_loki()
            print(f"\n✔ Valmis! Järjestelty {siirretty} tiedostoa. Undo-loki tallennettu.")
        else:
            print(f"\n✔ Simulaatio valmis. Ei tehty fyysisiä muutoksia.")

    def _tallenna_undo_loki(self):
        with open("undo_log.json", "w", encoding="utf-8") as f:
            json.dump(self.undo_loki, f, indent=4, ensure_ascii=False)

    @staticmethod
    def kumoa_siirrot():
        if not os.path.exists("undo_log.json"):
            print("❌ Undo-lokia (undo_log.json) ei löydy!")
            return
        
        with open("undo_log.json", "r", encoding="utf-8") as f:
            siirrot = json.load(f)

        print(f"🔄 Palautetaan {len(siirrot)} tiedostoa alkuperäisiin paikkoihinsa...")
        for merkinta in reversed(siirrot):
            lahde = merkinta["kohde"]
            kohde = merkinta["lahde"]
            if os.path.exists(lahde):
                os.makedirs(os.path.dirname(kohde), exist_ok=True)
                shutil.move(lahde, kohde)
        
        os.remove("undo_log.json")
        print("✔ Kaikki siirrot kumottu täydellisesti!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kvantti_loinen - Tiedostojärjestelmän eheyttäjä")
    parser.add_argument("--drive", type=str, default="F", help="Kohdeaseman kirjain (esim. F)")
    parser.add_argument("--dry-run", action="store_true", help="Suorita simulaatio tekemättä muutoksia")
    parser.add_argument("--undo", action="store_true", help="Palauta edellisen ajon tekemät siirrot")

    args = parser.parse_args()

    if args.undo:
        KvanttiLoinenGitHub.kumoa_siirrot()
    else:
        loinen = KvanttiLoinenGitHub(asema=args.drive, dry_run=args.dry_run)
        loinen.suorita()