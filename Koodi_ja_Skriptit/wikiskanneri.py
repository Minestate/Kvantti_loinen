import asyncio
from playwright.async_api import async_playwright

async def aja_skanneri():
    async with async_playwright() as p:
        # Käynnistetään selain
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Mennään Wikipediaan
        print("Yhdistetään Wikipediaan...")
        await page.goto("https://fi.wikipedia.org/wiki/Teko%C3%A4ly")

        # Otetaan valokopio (kuvakaappaus)
        print("Otetaan valokopio...")
        await page.screenshot(path="wikipedia_valokopio.png", full_page=True)

        # Otetaan teksti talteen
        sisalto = await page.content()
        with open("wikipedia_teksti.html", "w", encoding="utf-8") as f:
            f.write(sisalto)

        print("Valmis! Tiedostot tallennettu D-asemalle.")
        await browser.close()

asyncio.run(aja_skanneri())
