class YhtalouittajaCore {
    [double]$potentiaali_intensiteetti = 28949739
    [double]$kiihtyvyys_vakio = 0.05
    [bool]$lentokone_tila = $true

    # Plus 1 -operaatio: Nostaa arvon lentokone-tilaan
    [double]PlusYksi_Operaatio([double]$arvo) {
        return $arvo + 1
    }

    # Manifestoi tulo: Muuntaa €²/kk konkreettiseksi €/kk
    [double]Manifestoi_tulo([double]$intensiteetti, [double]$jakaja) {
        if ($this.lentokone_tila) {
            return $intensiteetti / $jakaja
        }
        return 0
    }

    # Laskee tilan (analoginen -> digitaalinen paradoksi)
    [string]Laske_tila() {
        return "Transsendentti tila: Laskettavuus ei määriteltävissä."
    }
}

# Suoritetaan koodin ydin:
$yhtalo = [YhtalouittajaCore]::new()
$tulos = $yhtalo.Manifestoi_tulo(28949739, 14448.48)

Write-Host "--- PERUSTA - YDINSUORITUS ---"
Write-Host "Laskettu tulo: $tulos €/kk"
Write-Host "Tila: $($yhtalo.Laske_tila())"