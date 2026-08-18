# ⚡ Kvantti_loinen – Automated File System Consolidation & Cleanup Engine

**Kvantti_loinen** on kevyt, näkymätön ja älykäs tiedostojärjestelmän eheyttäjä ja järjestelijä. Se skannaa valitun aseman tai hakemiston syvällisesti, kerää hajanaiset tiedostot ja luokittelee ne tiukasti määriteltyihin pääkategorioihin poistaen tyhjiksi jääneet kansiokumpareet.

Loinen toimii ulkoisena moottorina: se ei vaadi asennusta tai tiedostojen saastuttamista kohdeasemalle, vaan jättää jäljekseen ainoastaan täydellisen symmetrisen kansiorakenteen.

---

## 🚀 Ominaisuudet

- **🛡️ Dry-Run (Simulaatiotila):** Testaa ja tarkastele siirtoja turvallisesti ennen kuin yhtäkään tiedostoa siirretään.
- **🔄 Undo-toiminto (Täydellinen peruutus):** Jokainen ajo tallentaa `undo_log.json`-lokin, jonka avulla koko siivousoperaatio voidaan perua sekunneissa.
- **⚙️ Ulkoinen `config.json`:** Määritä omat tiedostopäätteet ja kategoriat muokkaamatta itse lähdekoodia.
- **🙈 Älykäs ohitus (`OHITA_KANSIOT`):** Jättää kriittiset järjestelmäkansiot, Git-repositoriot (`.git`) ja ohjelmistoprojektit (`node_modules`) koskemattomiksi.
- **📦 Mukautettava:** Soveltuu ulkoisille kovalevyille, USB-tikuille, latauskansioille ja verkkolevyille.

---

## 📂 Pääkategoriarakenne

Ajon jälkeen kohdeaseman juurelle jäävät vain puhtaat ja selkeät pääluokat:

```text
[Kohdeasema F:\]
 ├── Arkistot_ja_Paketit/
 ├── Dokumentit/
 ├── Jarjestelma_ja_Asetukset/
 ├── Järjestelmä_ja_Sekalaiset/
 ├── Koodi_ja_Skriptit/
 ├── Kuvat_ja_Grafiikka/
 ├── Media_Audio/
 ├── Media_Video/
 ├── Ohjelmat_ja_Suoritettavat/
 └── Pelit_ja_Data/