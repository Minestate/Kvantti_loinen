# build_perusta.ps1
Write-Host "Käynnistetään Perusta-OS-komponenttien kääntäminen..." -ForegroundColor Cyan

# Käännetään Java-ydin
javac -d ./out ./mother-program/Perusta-OS-main/*.java

if ($LASTEXITCODE -eq 0) {
    Write-Host "Käännös onnistui. Suoritetaan Trinity-Encore..." -ForegroundColor Green
    java -cp ./out TrinityEncore
} else {
    Write-Host "Käännösvirhe havaittu." -ForegroundColor Red
}