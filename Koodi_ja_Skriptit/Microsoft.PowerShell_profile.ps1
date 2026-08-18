# Automaattinen täydennys ja ennusteet
Import-Module PSReadLine
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView

# Ikonit Get-ChildItem (ls/dir) -komennolle
Import-Module Terminal-Icons

# Oh My Posh -teema (jos asennettu wingetillä)
if (Get-Command oh-my-posh -ErrorAction SilentlyContinue) {
    oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\jeblines.omp.json" | Invoke-Expression
}

# Hyödylliset oikotiet (aliakset)
function Edit-Profile { notepad $PROFILE }
Set-Alias -Name ep -Value Edit-Profile

function Update-AllModules { Update-Module -AcceptNextVersion -ErrorAction SilentlyContinue }
Set-Alias -Name upmod -Value Update-AllModules