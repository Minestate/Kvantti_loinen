import os
import shutil

class KvanttiMobiiliLoinen:
    def __init__(self, kohde_polku="/storage/emulated/0/Download"):
        self.kohde = kohde_polku

        # MOBIILILLE OPTIMOIDUT PÄÄKATEGORIAT
        self.FORMAATIT = {
            "Dokumentit": [".pdf", ".docx", ".doc", ".xlsx", ".txt", ".csv", ".epub"],
            "Kuvat": [".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic"],
            "Media": [".mp3", ".flac", ".wav", ".mp4", ".mkv", ".avi", ".mov"],
            "Asennustiedostot": [".apk", ".xapk", ".apks"],  # Mobiilispesifit paketit
            "Arkistot": [".zip", ".rar", ".7z", ".tar", ".gz"]
        }

    def _hae_kategoria(self, tiedosto):
        paate = os.path.splitext(tiedosto)[1].lower()
        if not paate:
            return "Ilman_Paatetta"
        for luokka, paatteet in self.FORMAATIT.items():
            if paate in paatteet:
                return luokka
        return "Muut_Tiedostot"

    def siivoa_mobiili(self):
        if not os.path.exists(self.kohde):
            print(f"❌ Polkua {self.kohde} ei löydy. Tarkista käyttöoikeudet.")
            return

        sallitut = set(self.FORMAATIT.keys())
        sallitut.update(["Ilman_Paatetta", "Muut_Tiedostot"])

        siirretty = 0

        for root, dirs, files in os.walk(self.kohde, topdown=False):
            # Suojataan pisteellä alkavat piilokansiot ja järjestelmäkansiot
            if "/." in root or "Android" in root:
                continue

            suhteellinen = os.path.relpath(root, self.kohde)
            paakansio = suhteellinen.split(os.sep)[0] if suhteellinen != "." else ""

            if paakansio in sallitut:
                continue

            for file in files:
                if file.startswith(".") or file.endswith(".tmp"):
                    continue

                lahde = os.path.join(root, file)
                kategoria = self._hae_kategoria(file)
                kohde_dir = os.path.join(self.kohde, kategoria)
                os.makedirs(kohde_dir, exist_ok=True)

                kohde = os.path.join(kohde_dir, file)
                
                if os.path.exists(kohde) and lahde != kohde:
                    nimi, paate = os.path.splitext(file)
                    kohde = os.path.join(kohde_dir, f"{nimi}_uusi{paate}")

                try:
                    shutil.move(lahde, kohde)
                    siirretty += 1
                except Exception as e:
                    print(f"⚠️ Ohitettiin {file}: {e}")

            # Tyhjät kansiot poistetaan vain lataushakemiston sisältä
            if root != self.kohde:
                try:
                    if not os.listdir(root):
                        os.rmdir(root)
                except Exception:
                    pass

        print(f"✔ Mobiilisiivous valmis! Järjestetty {siirretty} tiedostoa osoitteessa: {self.kohde}")

if __name__ == "__main__":
    # Esimerkki: Siivotaan Androidin Lataukset-kansio
    loinen = KvanttiMobiiliLoinen(kohde_polku="/storage/emulated/0/Download")
    loinen.siivoa_mobiili()
