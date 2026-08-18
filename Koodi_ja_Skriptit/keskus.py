import os
import sys
import time

class KilotavuEditori:
    """
    KilotavuEditori (Kilobyte Editor) ohjaa järjestelmän lokitusta.
    Säilöö datan ja logiikkajäljet kolmeen tasan 1024 tavun akkutiedostoon.
    """
    def __init__(self):
        self.akkutiedostot = ['par_1.dat', 'par_2.dat', 'par_3.dat']
        self.tavu_raja = 1024

    def mittaa_ram_kapasiteetti(self):
        """
        Mittaa järjestelmän fyysisen RAM-muistin gigatavuina.
        Palauttaa mitatun arvon suorituskykyprofiilin valintaa varten.
        """
        total_ram_gb = 16.0 # Oletus/Fallback-arvo
        
        try:
            if sys.platform.startswith('linux'):
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            kb = int(line.split()[1])
                            total_ram_gb = kb / (1024 * 1024)
                            break
            elif sys.platform == 'darwin':
                import subprocess
                total_ram_gb = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip()) / (1024**3)
        except Exception:
            pass # Käytetään turvallista fallback-arvoa, jos lukuoikeus estetty
            
        return total_ram_gb

    def tallenna_tila(self, kk, sisaan, ulos, saldo, profiili):
        """
        Pakkaa syklin tilan ja nykyisen MC-1 profiilin tasan 1024 tavun tiedostoihin.
        """
        lokidata = f"SYKLI_KK:{kk:02d}|IN:{sisaan:.2f}|OUT:{ulos:.2f}|BAL:{saldo:.2f}|PROF:{profiili}\n"
        
        for i, tiedosto in enumerate(self.akkutiedostot):
            lohko_sisalto = f"AKKU_{i+1}_LOGISET_JÄLJET\n" + lokidata
            paddatty_data = lohko_sisalto.encode('utf-8')
            
            if len(paddatty_data) < self.tavu_raja:
                paddatty_data += b'\x00' * (self.tavu_raja - len(paddatty_data))
            else:
                paddatty_data = paddatty_data[:self.tavu_raja]
                
            with open(tiedosto, 'wb') as f:
                f.write(paddatty_data)


class MobiiliControllerMC1:
    """
    MC-1 Mobiili-Controller (keskus.py)
    Hallitsee laitteen suorituskykyprofiileja, virrankulutusta ja CPU-skaalausta
    RAM-muistikapasiteetin sekä järjestelmän kuormituksen mukaan.
    """
    def __init__(self):
        self.nykyinen_profiili = "Alustamaton"
        self.cpu_taajuus = "Normaali"

    def aseta_profiili(self, ram_gb):
        """
        Määrittää suorituskykyprofiilin dynaamisesti mitatun RAM-muistin perusteella.
        """
        print("\n[MC-1] Analysoidaan laiteresursseja profiilin määritystä varten...")
        time.sleep(0.5)
        
        if ram_gb < 8.0:
            self.nykyinen_profiili = "SULJETTU (Kriittisen matala RAM)"
            self.cpu_taajuus = "Powersave"
            return False
        elif ram_gb < 12.0:
            self.nykyinen_profiili = "Ghost"
            self.cpu_taajuus = "Minimi (Säästötila)"
            print("[MC-1 TILA]: >> GHOST ACCESSED <<")
            print("-> Taustaprosessit jäädytetty. Akun ja muistin säästö maksimoitu.")
        elif ram_gb <= 16.0:
            self.nykyinen_profiili = "Eco"
            self.cpu_taajuus = "Balansoidut taajuudet"
            print("[MC-1 TILA]: >> ECO ACTIVE <<")
            print("-> Optimaalinen virrankulutus ja vakaa suorituskyky.")
        else:
            self.nykyinen_profiili = "Turbo"
            self.cpu_taajuus = "Maksimaaliset taajuudet (Performance)"
            print("[MC-1 TILA]: >> TURBO ENGAGED <<")
            print("-> Kaikki CPU-ytimet pakotettu täydelle teholle.")
            
        return True

    def suorita_ytimen_valvonta(self):
        """
        Simuloi MC-1 ohjaimen suorittamaa reaaliaikaista väylävalvontaa.
        """
        print(f"[MC-1 Valvonta] CPU Profiili: {self.nykyinen_profiili} | Ohjaustila: {self.cpu_taajuus}")


class PerustaSimulaatio:
    def __init__(self):
        self.osallistujat = 2200000
        self.kuukausimaksu = 138.95
        self.kesto_kk = 36
        self.palautus_erat = 9
        self.palautus_summa = 555.55
        
        self.kassavirta_sisaan = 0.0
        self.kassavirta_ulos = 0.0
        
        # Alustetaan osamoduulit
        self.editori = KilotavuEditori()
        self.mc1 = MobiiliControllerMC1()
        
    def aja_simulaatio(self):
        print("==================================================")
        print("=== PERUSTA JÄRJESTELMÄN KOKONAISARKKITEHTUURI ===")
        print("==================================================")
        
        # 1. Mitataan RAM-muisti KilotavuEditorilla
        mitattu_ram = self.editori.mittaa_ram_kapasiteetti()
        print(f"[Perusta] KilotavuEditori havaitsi laitteistossa: {mitattu_ram:.2f} GB RAM")
        
        # 2. Ohjataan mitattu arvo MC-1 Controllerille profiilin valintaa varten
        if not self.mc1.aseta_profiili(mitattu_ram):
            print("Kriittinen virhe: Järjestelmä vaatii vähintään 8 GB RAM-muistia.")
            return

        print(f"\n[Perusta] Aloitetaan 36 kuukauden talouskierron mekaaninen laskenta...")
        print("-" * 50)
        
        palautus_alkaa_kk = self.kesto_kk - self.palautus_erat + 1
        
        for kk in range(1, self.kesto_kk + 1):
            # Syklin matemaattinen siirto
            kuukausi_sisaan = self.osallistujat * self.kuukausimaksu
            self.kassavirta_sisaan += kuukausi_sisaan
            
            kuukausi_ulos = 0.0
            if kk >= palautus_alkaa_kk:
                kuukausi_ulos = self.osallistujat * self.palautus_summa
                self.kassavirta_ulos += kuukausi_ulos
                
            nykyinen_saldo = self.kassavirta_sisaan - self.kassavirta_ulos
            
            # Valvotaan suoritusta MC-1 ohjaimella ja lokitetaan KilotavuEditorilla
            if kk == 1 or kk == palautus_alkaa_kk or kk == self.kesto_kk:
                self.mc1.suorita_ytimen_valvonta()
                self.editori.tallenna_tila(kk, self.kassavirta_sisaan, self.kassavirta_ulos, nykyinen_saldo, self.mc1.nykyinen_profiili)
                
                print(f"Kuukausi {kk:02d} | Saldo: {nykyinen_saldo:,.2f} €")
                print("-" * 50)
            else:
                # Hiljainen lokitus taustalla (KilotavuEditori päivittää akut)
                self.editori.tallenna_tila(kk, self.kassavirta_sisaan, self.kassavirta_ulos, nykyinen_saldo, self.mc1.nykyinen_profiili)

        self.tulosta_loppuraportti()

    def tulosta_loppuraportti(self):
        loppusaldo = self.kassavirta_sisaan - self.kassavirta_ulos
        print("\n==================================================")
        print("===           SÝKLIN LOPPURAPORTTI             ===")
        print("==================================================")
        print(f"Kokonaiskertymä (Sisään):  {self.kassavirta_sisaan:,.2f} €")
        print(f"Kokonaispalautus (Ulos):   {self.kassavirta_ulos:,.2f} €")
        print(f"Järjestelmään jäävä saldo: {loppusaldo:,.2f} €")
        
        odotettu_jannos = 4950000.00
        if abs(loppusaldo - odotettu_jannos) < 0.01:
            print(f"\n> TILA: MATEMAATTINEN TASAPAINO LUKITTU ({odotettu_jannos:,.2f} €).")
            print("> MC-1 ohjain siirtää laitteiston ylläpitotilaan.")
        else:
            print("\n> VAROITUS: Matemaattisessa mallissa poikkeama.")

if __name__ == "__main__":
    perusta = PerustaSimulaatio()
    perusta.aja_simulaatio()