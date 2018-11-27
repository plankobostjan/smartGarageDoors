# Ideje

## Projekt ima veliko možnosti razširitev:
  - Odpiranje vrat s prstnim odtisom
  - Opdiranje/zaprianje vrat, če je v garaži pretoplo/premrzlo
  - Preverjanje ali je avto v garaži ali ne
  - Spremljanje stanja vrat preko spleta
  - Pošiljanje obvestil o stanju/spremembi stanja garažnih vrat
  - Samodejno zapiranje vrat ob deločenem času

## Programske rešitve
### #1 En program ali več programov?
Kaj je boljše? Imeti en program, ki bo nadzoroval vse ali imeti več programov, ki bodo nadzorovali vsak svojo stvar.
Na to vprašanje bom najlažje ugotovil tekom dela, ko bom videl kaj je lažje in bolj praktično.
### #2 Telegram bot
Ideja je, da napišem bota, ki bo tekel na Raspberry Pi. Z njim bo mogoče preveriti stanje garažnih vrat oziroma garaže.
Vprašanja, možne težave/omejitve:
- je varno dostopati do garažnih vrat preko spleta?
- so lahko Telegram boti zasebni ali so vsi javni?
- kakšne so možnosti, da si nekdo preko bota omogoči dostop do strežnika?
- alternative Telegram botu?

### #3 Android aplikacija
Izdelati Android aplikacijo za upravljanje garažnih vrat, uporavljanje le teh in preverjanje stanja v garaži.

Problem: Kako dostopati do podatkov/programov strežnika preko Android aplikacije?

Možne rešitve:
- preko spletnega strežnika
- preko ssh
- preko Telegram bota??
- preko API

### #4 API
Bo potrebno napisati API? Ali obstajajo še druge možnosti komunikacije med aplikacijo in strežnikom?
