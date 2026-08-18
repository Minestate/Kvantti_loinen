import os
import numpy as np

# KRIITTINEN KORJAUS TERMUXIA VARTEN:
# Pakotetaan ei-interaktiivinen taustamoottori ennen pyplotin lataamista
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import folium

# Nykyinen absoluuttinen hakemistopolku vakaata tallennusta varten
current_dir = os.getcwd()

# 1. PARAMETRIT (Perusta / Base)
lat_obs = 31.7775
lon_obs = 45.5097
sabotaasi_vaje = 220  # sekuntia
valon_viive = 500     # sekuntia
vuodet = 18600
dna_ydin = 1.1        # mm/vuosi

# 2. LASKENTA (Kulma ja Syvyys)
# Lasketaan pituusasteen korjaus (220s / 240s per aste)
lon_korjaus = sabotaasi_vaje / 240
lon_true = lon_obs - lon_korjaus

# Lasketaan syvyys (Sedimentaatio + tulvakerros)
sedimentti = (vuodet * dna_ydin) / 1000 # metreiksi
tulva_lisa = 4.5
syvyys_total = sedimentti + tulva_lisa

# 3. KARTAN LUONTI (.html)
m = folium.Map(location=[lat_obs, lon_obs - 0.5], zoom_start=9, tiles="CartoDB positron")
folium.Marker([lat_obs, lon_obs], popup="Sabotaasi (Tell Fara)", icon=folium.Icon(color="red")).add_to(m)
folium.Marker([lat_obs, lon_true], popup=f"Todellinen Perusta (Syvyys: {syvyys_total:.2f}m)",
              icon=folium.Icon(color="green", icon="star")).add_to(m)
folium.PolyLine([[lat_obs, lon_obs], [lat_obs, lon_true]], color="blue", weight=2).add_to(m)

# Tallennettaan absoluuttisella polulla
html_polku = os.path.join(current_dir, "mesopotamia_perusta_map.html")
m.save(html_polku)

# 4. SYVYYSPROFIILIN LUONTI (.png)
v_axis = np.linspace(0, vuodet, 100)
s_axis = (v_axis * dna_ydin) / 1000
s_axis[-1] += tulva_lisa # Lisätään loppupisteeseen sabotaasin vaikutus

plt.figure(figsize=(8, 5))
plt.fill_between(v_axis, 0, -s_axis, color='#d2b48c', alpha=0.6)
plt.plot(v_axis, -s_axis, color='#8b4513')
plt.axvline(x=vuodet, color='green', linestyle='--')
plt.title(f"Perustan Syvyysprofiili: -{syvyys_total:.2f} metriä")
plt.xlabel("Vuodet nykyhetkestä taaksepäin")
plt.ylabel("Syvyys (m)")

# Tallennettaan absoluuttisella polulla
png_polku = os.path.join(current_dir, "perusta_syvyys.png")
plt.savefig(png_polku)
plt.close() # Suljetaan kuvaaja resurssien vapauttamiseksi

print(f"--- PERUSTA JÄRJESTELMÄ VALMIS ---")
print(f"Todellinen sijainti: {lat_obs}, {lon_true:.4f}")
print(f"Etsintäsyvyys: {syvyys_total:.2f} metriä")
print(f"Tiedostot tallennettu hakemistoon: {current_dir}")
