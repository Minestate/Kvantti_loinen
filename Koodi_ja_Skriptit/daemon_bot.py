import asyncio

# Asetetaan ajastussekunnit (esim. 3600 s = 1 tunti)
RUN_INTERVAL_SECONDS = 3600  

async def autonomous_loop():
    start_site = "https://news.ycombinator.com"
    
    while True:
        print("\n[OMA-ALOITTEINEN BOTTI] Aloitetaan uusi tarkistuskierros...")
        
        # Käynnistetään keräys- ja pakkausprosessi
        bot = AsyncAdCrawlerBot(start_url=start_site, max_pages=10)
        await bot.run()
        
        print(f"\n[OMA-ALOITTEINEN BOTTI] Kierros valmis. Odotetaan {RUN_INTERVAL_SECONDS / 60} minuuttia ennen seuraavaa ajokertaa...")
        
        # Odotetaan määritetty aika ennen seuraavaa oma-aloitteista kierrosta
        await asyncio.sleep(RUN_INTERVAL_SECONDS)

if __name__ == "__main__":
    # Käynnistetään ikuinen taustasilmukka
    try:
        asyncio.run(autonomous_loop())
    except KeyboardInterrupt:
        print("\nBotti pysäytetty manuaalisesti.")