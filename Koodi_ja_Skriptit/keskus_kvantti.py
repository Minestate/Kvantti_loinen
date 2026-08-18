from dna_ydin import hae_ydin, injektoi
import curses
import time

class KvanttiAndroidSimu:
    def __init__(self):
        # 7 näyttöä, joissa jokaisessa on Suora, Käänteinen ja Menevä tila
        self.sanat = ["AUTONOM", "PERUSTA", "YDIN_OK", "TASAPAI", "TEKOÄLY", "RELE_4D", "MEKAANI"]
        self.lepo_naytto = 0

    def aja_simulaatio(self, stdscr):
        # Alustetaan curses-ikkunan asetukset
        curses.curs_set(0) # Piilotetaan tekstikursori
        stdscr.nodelay(True) # Ei jäädä odottamaan näppäinpainallusta (lennosta ajo)
        stdscr.timeout(100) # Päivitysnopeus 100ms (99% -> 100% vakaus)

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            # Otsikkokehä (5D Käsitteellinen taso)
            stdscr.addstr(0, 2, "=== ANDROID KVANTTI-JÄRJESTELMÄ (TERMUX-CORE) ===", curses.A_BOLD)
            stdscr.addstr(1, 2, "6 Nanokonetta + 1 Käyttäjä (Sinä) | 1:2 Liukumamatriisi")
            stdscr.addstr(2, 2, "--------------------------------------------------------")

            # Päivitetään se lepovaihteen siirtymä (6 nanokonetta vs 7 näyttöä)
            self.lepo_naytto = (self.lepo_naytto + 1) % 7

            # Piirretään 7 segmenttinäyttöä lennosta
            for i in range(7):
                y_pos = 4 + (i * 2)
                if y_pos >= h - 2:
                    break

                sana = self.sanat[i]
                kaanteinen = sana[::-1]
                meneva = f"{sana[3:]}{sana[:3]}"

                if i == self.lepo_naytto:
                    # Nollapiste / Salpaustila lepovirrassa
                    stdscr.addstr(y_pos, 2, f"NÄYTTÖ {i} [SALPA] ──► [ BIOS-PARISTO VAKAA ] ──► (99% LEPOTEHO)")
                else:
                    # Aktiivinen 1:2 liukutila, jossa käänteisresurssi on valmiina
                    stdscr.addstr(y_pos, 2, f"NÄYTTÖ {i} [S: {sana:7}] ◄─► [K: {kaanteinen:7}] ◄─► [M: {meneva:7}] ─► 100%")

            stdscr.addstr(19, 2, "--------------------------------------------------------")
            stdscr.addstr(20, 2, "Paina 'I' antaaksesi IMPULSSIN (Numero 1) tai 'Q' sulkeaksesi.")

            # Tarkistetaan käyttäjän (Puuttuva Numero 1) tietoinen vuorovaikutus
            try:
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('i') or key == ord('I'):
                    # Käyttäjä lyö tyhjiöön uuden järjestyksen
                    self.sanat = self.sanat[1:] + [self.sanat[0]]
                    stdscr.addstr(21, 2, "[IMPULSSI] Kosketus havaittu! Rakenne liikahti 120 astetta.", curses.A_REVERSE)
                    stdscr.refresh()
                    time.sleep(0.4)
            except Exception:
                pass

            stdscr.refresh()

if __name__ == "__main__":
    simu = KvanttiAndroidSimu()
    # Käynnistetään curses-moottori fyysiselle raudalle
    curses.wrapper(simu.aja_simulaatio)
    print("\n[Perusta] Kvanttisimulaatio suljettu onnistuneesti. Tila tallennettu.")
