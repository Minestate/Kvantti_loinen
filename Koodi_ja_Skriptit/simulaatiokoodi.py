import sys

class PerustaSimulaatio:
    def __init__(self):
        # Perusparametrit ja kiinteät reuna-arvot
        self.osallistujat = 2200000
        self.kuukausimaksu = 138.95
        self.kesto_kk = 36
        
        # Palautusjärjestelmän parametrit (9 erää)
        self.palautus_erat = 9
        self.palautus_summa = 555.55
        
        # Järjestelmän sisäiset tilit
        self.kassavirta_sisaan = 0.0
        self.kassavirta_ulos = 0.0
        
    def aja_simulaatio(self):
        print("=== PERUSTA - TALOUDELLISEN SYKLIEN SIMULAATIO ===")
        print(f"Osallistujamäärä: {self.osallistujat:,} henkilöä")
        print(f"Kuukausierä: {self.kuukausimaksu} € / kk")
        print(f"Kesto: {self.kesto_kk} kuukautta")
        print("-" * 50)
        
        # Lasketaan palautuskuukaudet siten, että ne jakautuvat tasaisesti tai 
        # kohdistuvat syklin loppupuolelle (esim. viimeiset 9 kuukautta)
        palautus_alkaa_kk = self.kesto_kk - self.palautus_erat + 1
        
        for kk in range(1, self.kesto_kk + 1):
            # 1. Kuukausittainen sisäänvirtaus
            kuukausi_sisaan = self.osallistujat * self.kuukausimaksu
            self.kassavirta_sisaan += kuukausi_sisaan
            
            # 2. Kuukausittainen ulosvirtaus (jos palautusikkunassa)
            kuukausi_ulos = 0.0
            if kk >= palautus_alkaa_kk:
                kuukausi_ulos = self.osallistujat * self.palautus_summa
                self.kassavirta_ulos += kuukausi_ulos
                
            nykyinen_saldo = self.kassavirta_sisaan - self.kassavirta_ulos
            
            # Tulostetaan tilannekuva kriittisistä vaiheista (alku, palautuksen alkaminen, loppu)
            if kk == 1 or kk == palautus_alkaa_kk or kk == self.kesto_kk:
                print(f"Kuukausi {kk:02d}:")
                print(f"  Kerätty tähän mennessä: {self.kassavirta_sisaan:,.2f} €")
                print(f"  Palautettu tähän mennessä: {self.kassavirta_ulos:,.2f} €")
                print(f"  Järjestelmän nykytila: {nykyinen_saldo:,.2f} €")
                print("-" * 50)

        self.tulosta_loppuraportti()

    def tulosta_loppuraportti(self):
        loppusaldo = self.kassavirta_sisaan - self.kassavirta_ulos
        
        print("\n=== SIMULAATION LOPPURAPORTTI ===")
        print(f"Kokonaiskertymä (Sisään):  {self.kassavirta_sisaan:,.2f} €")
        print(f"Kokonaispalautus (Ulos):   {self.kassavirta_ulos:,.2f} €")
        print(f"Järjestelmään jäävä saldo: {loppusaldo:,.2f} €")
        
        # Verifioidaan nollatilan tasapaino ja mekaaninen jäännös
        odotettu_jannos = 4950000.00
        if abs(loppusaldo - odotettu_jannos) < 0.01:
            print("\n> TILA: MATEMAATTINEN TASAPAINO SAAVUTETTU.")
            print(f"> Järjestelmän mekaaninen suojajäännös on täsmälleen {odotettu_jannos:,.2f} €.")
        else:
            print("\n> VAROITUS: Epätasapaino matemaattisessa mallissa.")

if __name__ == "__main__":
    simu = PerustaSimulaatio()
    simu.aja_simulaatio()