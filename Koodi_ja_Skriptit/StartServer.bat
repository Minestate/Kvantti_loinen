@echo off
:loop
echo Kaynnistetaan Killing Floor -palvelinta...
cd /d C:\KFServer\System
ucc.exe server KF-BioticsLab.rom?game=KFmod.KFGameType?VACSecured=true?MaxPlayers=6 -log=server.log
echo Palvelin kaatui tai suljettiin, kaynnistetaan uudelleen...
goto loop