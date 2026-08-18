Import-Module Terminal-Icons
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\jeblines.omp.json" | Invoke-Expression
# Nopeampi kansion selaus
Set-Alias -Name l -Value Get-ChildItem

# Pika-avaukset
function Edit-Profile { notepad $PROFILE }
Set-Alias -Name ep -Value Edit-Profile

# Luotettava verkkoyhteyden pikatesti
function Ping-Google { Test-NetConnection google.com }
Set-Alias -Name png -Value Ping-Google

# Järjestelmän pikapuhdistus (vapaa muisti ja prosessit)
function Get-TopMemory { Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 }
Set-Alias -Name topmem -Value Get-TopMemory
function Update-AllModules { Update-Module -AcceptNextVersion -ErrorAction SilentlyContinue }
Set-Alias -Name upmod -Value Update-AllModules
# Import the Chocolatey Profile that contains the necessary code to enable
# tab-completions to function for `choco`.
# Be aware that if you are missing these lines from your profile, tab completion
# for `choco` will not function.
# See https://ch0.co/tab-completion for details.
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}
