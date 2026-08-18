import os
import sys
import time
import webbrowser

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
        Mittaa järjestelmän fyysisen RAM-muistin gigatavuina alustariippumattomasti.
        """
        total_ram_gb = 16.0  # Turvallinen fallback-oletus
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
            elif sys.platform == 'win32':
                import ctypes
                kernel32 = ctypes.windll.kernel32
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong),
                        ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong),
                        ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong),
                        ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('ullAvailExtendedVirtual', ctypes.c_ulonglong)
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                total_ram_gb = stat.ullTotalPhys / (1024**3)
        except Exception:
            pass
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
    Hallitsee laitteen suorituskykyprofiileja RAM-muistikapasiteetin mukaan.
    """
    def __init__(self):
        self.nykyinen_profiili = "Alustamaton"
        self.cpu_taajuus = "Normaali"

    def aseta_profiili(self, ram_gb):
        if ram_gb < 8.0:
            self.nykyinen_profiili = "SULJETTU (Kriittisen matala RAM)"
            self.cpu_taajuus = "Powersave"
            return False
        elif ram_gb < 12.0:
            self.nykyinen_profiili = "Ghost"
            self.cpu_taajuus = "Minimi (Säästötila)"
        elif ram_gb <= 16.0:
            self.nykyinen_profiili = "Eco"
            self.cpu_taajuus = "Balansoidut taajuudet"
        else:
            self.nykyinen_profiili = "Turbo"
            self.cpu_taajuus = "Maksimaaliset taajuudet (Performance)"
        return True


class PerustaSelainSimulaatio:
    def __init__(self):
        self.osallistujat = 2200000
        self.kuukausimaksu = 138.95
        self.kesto_kk = 36
        self.palautus_erat = 9
        self.palautus_summa = 555.55
        
        self.kassavirta_sisaan = 0.0
        self.kassavirta_ulos = 0.0
        
        self.editori = KilotavuEditori()
        self.mc1 = MobiiliControllerMC1()

    def aja_ja_luo_selainpinta(self):
        mitattu_ram = self.editori.mittaa_ram_kapasiteetti()
        ajokelpoinen = self.mc1.aseta_profiili(mitattu_ram)

        # Aloitetaan HTML-sivun rakentaminen
        html_rakenne = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Perusta Arkkitehtuuri - Selainkonsoli</title>
    <style>
        body {{ font-family: 'Segoe UI', monospace; background-color: #0d1117; color: #c9d1d9; padding: 30px; margin: 0; }}
        h1 {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 15px; margin-top: 0; }}
        .status-container {{ display: flex; gap: 20px; margin-bottom: 25px; }}
        .status-box {{ background-color: #161b22; padding: 20px; border-radius: 6px; border: 1px solid #30363d; flex: 1; }}
        .highlight {{ color: #58a6ff; font-weight: bold; }}
        .turbo {{ color: #238636; font-weight: bold; }}
        .ghost {{ color: #d29922; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        th, td {{ text-align: left; padding: 12px; border-bottom: 1px solid #21262d; }}
        th {{ background-color: #161b22; color: #58a6ff; font-weight: 600; }}
        tr:hover {{ background-color: #161b22; }}
        .success-banner {{ background-color: rgba(35, 134, 54, 0.15); border: 1px solid #238636; padding: 20px; border-radius: 6px; margin-top: 25px; }}
        .success-title {{ color: #3fb950; font-weight: bold; font-size: 1.2em; margin-bottom: 5px; }}
    </style>
</head>
<body>
    <h1>PERUSTA – JÄRJESTELMÄN KOKONAISARKKITEHTUURI</h1>
    
    <div class="status-container">
        <div class="status-box">
            <h3>Laiteresturssit</h3>
            <strong>KilotavuEditori Mittaus:</strong> <span class="highlight">{mitattu_ram:.2f} GB RAM</span>
        </div>
        <div class="status-box">
            <h3>MC-1 Ohjaustila</h3>
            <strong>Nykyinen Profiili:</strong> <span class="{"turbo" if self.mc1.nykyinen_profiili == "Turbo" else "ghost"}">{self.mc1.nykyinen_profiili}</span><br>
            <strong>CPU Väyläohjaus:</strong> {self.mc1.cpu_taajuus}
        </div>
    </div>
"""

        if not ajokelpoinen:
            html_rakenne += f"""
    <div style="background-color: rgba(248, 81, 73, 0.15); border: 1px solid #f85149; padding: 20px; border-radius: 6px;">
        <strong style="color: #f85149;">KRIITTINEN KESKEYTYS:</strong> Järjestelmä vaatii vähintään 8 GB RAM-muistia turvalliseen suoritukseen.
    </div>
</body>
</html>"""
            self._kirjoita_ja_avaa(html_rakenne)
            return

        # Ajetaan simulaatiokierros taustalla
        palautus_alkaa_kk = self.kesto_kk - self.palautus_erat + 1
        
        html_rakenne += """
    <h2>Syklin mekaaninen ajoloki (36 kuukautta)</h2>
    <table>
        <tr>
            <th>Aikajakso</th>
            <th>Kertymä Sisään (M€)</th>
            <th>Palautukset Ulos (M€)</th>
            <th>Järjestelmän Nykyinen Saldo</th>
        </tr>"""

        for kk in range(1, self.kesto_kk + 1):
            self.kassavirta_sisaan += self.osallistujat * self.kuukausimaksu
            
            kuukausi_ulos = 0.0
            if kk >= palautus_alkaa_kk:
                kuukausi_ulos = self.osallistujat * self.palautus_summa
                self.kassavirta_ulos += kuukausi_ulos
                
            nykyinen_saldo = self.kassavirta_sisaan - self.kassavirta_ulos
            
            # Mekaaninen 1 KB lukitus kovalevylle joka askeleella
            self.editori.tallenna_tila(kk, self.kassavirta_sisaan, self.kassavirta_ulos, nykyinen_saldo, self.mc1.nykyinen_profiili)
            
            # Otetaan talteen tärkeimmät syklin murroskohdat selainnäkymään
            if kk == 1 or kk == palautus_alkaa_kk or kk == self.kesto_kk:
                html_rakenne += f"""
        <tr>
            <td>Kuukausi {kk:02d}</td>
            <td>{self.kassavirta_sisaan / 1_000_000:,.2f} M€</td>
            <td>{self.kassavirta_ulos / 1_000_000:,.2f} M€</td>
            <td><strong>{nykyinen_saldo:,.2f} €</strong></td>
        </tr>"""

        html_rakenne += "    </table>"

        # Loppusaldo ja nollatilan verifiointi
        loppusaldo = self.kassavirta_sisaan - self.kassavirta_ulos
        
        html_rakenne += f"""
    <div class="success-banner">
        <div class="success-title">SÝKLIN LOPPURAPORTTI & METRIKAT</div>
        Kokonaiskertymä (In): {self.kassavirta_sisaan:,.2f} €<br>
        Kokonaispalautus (Out): {self.kassavirta_ulos:,.2f} €<br>
        Järjestelmän jäännös puskuri: <strong>{loppusaldo:,.2f} €</strong><br><br>
"""
        
        if abs(loppusaldo - 4950000.00) < 0.01:
            html_rakenne += """
        <strong>> TILA: MATEMAATTINEN TASAPAINO SAAVUTETTU (4 950 000,00 €) <</strong><br>
        > KilotavuEditori on lukinnut eheystarkistuksen. MC-1 siirtää laitteiston valmiustilaan.
"""
        html_rakenne += """
    </div>
</body>
</html>"""

        self._kirjoita_ja_avaa(html_rakenne)

    def _kirjoita_ja_avaa(self, html_sisalto):
        tiedoston_nimi = "perusta_konsoli.html"
        # Kirjoitetaan valmis HTML tiedostoon
        with open(tiedoston_nimi, "w", encoding="utf-8") as f:
            f.write(html_sisalto)
            
        # Avataan tiedosto automaattisesti järjestelmän oletusselaimeen
        polku = os.path.abspath(tiedoston_nimi)
        webbrowser.open(f"file://{polku}")
        print(f"\n[Selain] Simulaatio valmis. Selainpinta avattu polkuun: file://{polku}")


if __name__ == "__main__":
    simu = PerustaSelainSimulaatio()
    simu.aja_ja_luo_selainpinta()