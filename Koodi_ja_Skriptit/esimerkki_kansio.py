import os
import json
import zipfile
import hashlib
import shutil

class KvanttiLoisCore:
    def __init__(self, target_folder, secret_key):
        self.folder = target_folder
        self.secret_key = secret_key
        self.master_hash = hashlib.sha256(secret_key.encode()).hexdigest()
        self.archive_path = os.path.join(self.folder, "standby_bots.zip")

    def suorita_siivous_ja_jauhanne(self):
        print(f"=== KÄYNNISTETÄÄN KANSIO SIIVOUS: {self.folder} ===")
        
        # 1. Tarkistetaan onko aiempaa pakettia ja puretaan jos löytyy
        if os.path.exists(self.archive_path):
            with zipfile.ZipFile(self.archive_path, 'r') as zipf:
                zipf.extractall(self.folder)
            os.remove(self.archive_path)
            print("[✔] Omat botit purettu käyttöön.")
        else:
            # Luodaan READ_ME-simulaatiokansio ensimmäisellä kerralla
            readme_dir = os.path.join(self.folder, "READ_ME")
            os.makedirs(readme_dir, exist_ok=True)
            with open(os.path.join(readme_dir, "LUE_MINUT.txt"), "w", encoding="utf-8") as f:
                f.write("Tämä kansio sisältää kvantti_loisen toimintaohjeet ja simulaatioraportin.\n")

        # 2. Säilytetään vieraat tiedostot ja järjestellään ne tyypin mukaan
        own_items = ["READ_ME", "non_bot.json", "npc_bot.json", "pvp_bot.json", "standby_bots.zip", "Sailytetyt_Vieraat"]
        saatavat_vieraat = []

        for item in os.listdir(self.folder):
            if item in own_items:
                continue

            item_path = os.path.join(self.folder, item)
            if os.path.isfile(item_path):
                ext = item.split(".")[-1].upper() if "." in item else "TUNDEMATON"
                kohde_kansio = os.path.join(self.folder, "Sailytetyt_Vieraat", f"Tiedostot_{ext}")
                os.makedirs(kohde_kansio, exist_ok=True)
                
                shutil.move(item_path, os.path.join(kohde_kansio, item))
                saatavat_vieraat.append(item)

        print(f"[✔] Säilytetty {len(saatavat_vieraat)} vierasta tiedostoa turvassa.")

        # 3. Jauhetaan omat tiedostot .json-muotoon kvantti_loiselle
        non_data = {"type": "non_bot", "vieraat_turvassa": saatavat_vieraat, "lkm": len(saatavat_vieraat)}
        npc_data = {"type": "npc_bot", "tila": "SIIVOUS_SUORITETTU", "automaattinen": True}
        pvp_data = {"type": "pvp_bot", "expected_master_hash": self.master_hash, "tila": "STANDBY"}

        with open(os.path.join(self.folder, "non_bot.json"), "w", encoding="utf-8") as f:
            json.dump(non_data, f, indent=4)
        with open(os.path.join(self.folder, "npc_bot.json"), "w", encoding="utf-8") as f:
            json.dump(npc_data, f, indent=4)
        with open(os.path.join(self.folder, "pvp_bot.json"), "w", encoding="utf-8") as f:
            json.dump(pvp_data, f, indent=4)

        # 4. Pakataan jauhetut .json-tiedostot valmiustilaan ja siivotaan irralliset pois
        bot_files = ["non_bot.json", "npc_bot.json", "pvp_bot.json"]
        with zipfile.ZipFile(self.archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for b_file in bot_files:
                file_path = os.path.join(self.folder, b_file)
                zipf.write(file_path, arcname=b_file)
                os.remove(file_path)

        print(f"[🔒] Omat tiedostot jauhettu JSONiksi ja lukittu pakettiin: {self.archive_path}\n")


# =================================================================
# TESTIAJO ESIMERKKIKANSIOLLA
# =================================================================
if __name__ == "__main__":
    TESTI_KANSIO = "./Esimerkki_Sotkuinen_Kansio"
    AVAIN = "Kvantti_Avain_2026"

    # 1. Luodaan esimerkkikansio ja sinne "sotkua" (vieraat tiedostot)
    os.makedirs(TESTI_KANSIO, exist_ok=True)
    
    sotkutiedostot = ["raportti.pdf", "loma_kuva.png", "muistiinpanot.txt", "projekti.docx", "perhekuva.jpg"]
    for tiedosto in sotkutiedostot:
        with open(os.path.join(TESTI_KANSIO, tiedosto), "w", encoding="utf-8") as f:
            f.write("Tämä on käyttäjän vieras tiedosto.")

    print("--> Esimerkkikansio luotu ja täytetty vierain tiedostoin.")

    # 2. Ajetaan kvantti_loisen siivous ja jauhanne
    loinen = KvanttiLoisCore(TESTI_KANSIO, AVAIN)
    loinen.suorita_siivous_ja_jauhanne()