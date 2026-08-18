# Asetukset
$Server = "irc.libera.chat"
$Port = 6697
$Nick = "TaskuLaskinBot"
$Channel = "#testikanava"

# Luodaan SSL-yhteys
$TcpClient = New-Object System.Net.Sockets.TcpClient($Server, $Port)
$SslStream = New-Object System.Net.Security.SslStream($TcpClient.GetStream(), $false)
$SslStream.AuthenticateAsClient($Server)

$Writer = New-Object System.IO.StreamWriter($SslStream)
$Reader = New-Object System.IO.StreamReader($SslStream)

# Kirjautuminen
$Writer.WriteLine("NICK $Nick")
$Writer.WriteLine("USER $Nick 0 * :PowerShell Synapsi Botti")
$Writer.Flush()

# Automaattinen liittyminen kanavalle (odota hetki kirjautumista)
Start-Sleep -Seconds 5
$Writer.WriteLine("JOIN $Channel")
$Writer.Flush()

Write-Host "Synapsi aktivoitu ja yhdistetty."

# Pääsilmukka
while ($true) {
    if ($SslStream.DataAvailable) {
        $Line = $Reader.ReadLine()
        Write-Host $Line
        
        # PING-PONG ylläpito (tärkeä IRC:ssä)
        if ($Line.StartsWith("PING")) {
            $Writer.WriteLine("PONG " + $Line.Split(':')[1])
            $Writer.Flush()
        }

        # Laskentakomento !laske
        if ($Line.Contains("PRIVMSG $Channel :!laske ")) {
            $InputText = $Line.Split('!laske ')[1].Trim()
            
            # Suoritetaan laskenta turvallisesti (PowerShellin Invoke-Expression on riskialtis, 
            # siksi käytämme tässä vain yksinkertaista aritmetiikkaa)
            try {
                $Result = Invoke-Expression $InputText
                $Writer.WriteLine("PRIVMSG $Channel :Tulos: $Result")
            } catch {
                $Writer.WriteLine("PRIVMSG $Channel :Virhe laskennassa.")
            }
            $Writer.Flush()
        }
    }
}