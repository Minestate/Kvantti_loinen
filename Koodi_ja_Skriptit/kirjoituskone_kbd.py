from dna_ydin import hae_ydin, injektoi
import curses
import time

class KirjoituskoneTeema:
    def __init__(self):
        # Mekaanisen kirjoituskoneen porrastetut rivit
        self.rivi1 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
        self.rivi2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
        self.rivi3 = ["Z", "X", "C", "V", "B", "N", "M"]
        self.paperi = "" # Mitä kirjoituskoneeseen on tulostunut

    def piirra_nayttis(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False) # Odotetaan tietoisen käyttäjän painallusta

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            # Telatila / Paperi (Mihin teksti iskeytyy metallivarrella)
            stdscr.addstr(1, 2, "=== MEKAANINEN TEEMANÄPPÄIMISTÖ: TELATILA ===", curses.A_BOLD)
            stdscr.addstr(3, 4, f"PAPERI: {self.paperi if self.paperi else '[Tyhjä tela]'}", curses.A_UNDERLINE)
            stdscr.addstr(5, 2, "--------------------------------------------------------")

            # Piirretään mekaaniset pyöreät näppäimet porrastetusti
            # Rivi 1
            r1_str = "   ".join([f"({k})" for k in self.rivi1])
            stdscr.addstr(8, 4, r1_str)

            # Rivi 2 (Siirretty oikealle – aito mekaaninen porrastus)
            r2_str = "   ".join([f"({k})" for k in self.rivi2])
            stdscr.addstr(10, 6, r2_str)

            # Rivi 3 (Siirretty vielä enemmän oikealle)
            r3_str = "   ".join([f"({k})" for k in self.rivi3])
            stdscr.addstr(12, 8, r3_str + "   (⌫)")

            # Rivi 4 (Välilyönti ja toimintavivut)
            stdscr.addstr(14, 4, "[CTRL]   [============ SPACE ============]   [RETURN]")
            stdscr.addstr(16, 2, "--------------------------------------------------------")
            stdscr.addstr(17, 2, "Paina näppäintä. ESC sulkee näppäimistön ja lukitsee teeman.")

            stdscr.refresh()

            # Luetaan painallus
            ch = stdscr.getch()

            # ESC eli koodi 27 sulkee järjestelmän
            if ch == 27:
                break
            # Backspace / Pyyhintä
            elif ch in (127, 8, curses.KEY_BACKSPACE):
                self.paperi = self.paperi[:-1]
            # Välilyönti
            elif ch == ord(' '):
                self.paperi += " "
            # Kirjaimet (Muutetaan isoksi tekstiksi kuten kirjoituskoneessa)
            elif 32 <= ch <= 126:
                kirjain = chr(ch).upper()
                self.paperi += kirjain
                
                # Simuloidaan mekaanista iskua ja viivettä (Restauraatio)
                stdscr.addstr(3, 4, f"PAPERI: {self.paperi} *KLAK*", curses.A_BOLD)
                stdscr.refresh()
                time.sleep(0.05)

if __name__ == "__main__":
    teema = KirjoituskoneTeema()
    curses.wrapper(teema.piirra_nayttis)
    print("\n[Perusta] Kirjoitustila suljettu. Teemanäppäimistön asettelu tallennettu.")
