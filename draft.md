# Pametna garažna vrata

## Uvod
### Opis problema

Problem današnjih garažnih vrat je, da jih je običajni možno odpreti samo na dva načina. S priloženim daljincem ali s tipko, običajno nameščeno na notranji strani garažnih vrat. Če želimo torej garana vrata odpretni moramo bitjt ali v garaži ali pa moramo imeti pri sebi daljinec. To pa je v vsakdanjem življenju nepraktično, sploh v primeru, ko pri hiši živi veliko ljudi, vsi pa rabijo dostop do garaže.

V tej nalogi bom predstavil svojo idejo, pametna garažna vrata, kot sem si jih zamislil in poskušal realizirati.

### Teze
Za raziskovalno nalogo, sem si postavil naslednje teze
  - Garažna vrata bo možno upravljati preko telefona
  - Garažna vrata bo možno upravljati preko spletne strani
  - Raspberry Pi bo spremljal ali je avto v garaži ali ne in glede na to samodejno zapiral garažna vrata
  - Raspberry Pi bo spremljal temperaturo v garaži in jih samodejno zaprl v primeru prenizke ali previsoke temperature
  - Raspberry Pi bo samodejno zaprl garažna vrata, če ostanejo odprta po določeni uri
  - Raspberry Pi nas bo preko potisnih obvestil obveščal o spremembi stanja garažnih vrat
  - Raspberry Pi bo beležil kdo in kdaj je aktiviral garažna vrata
  
  ### Raziskovalne metode
  Najprej sem z metodo raziskovanja raziskal katere komponente bi bilo smiselno uporabiti za realizacijo raziskovalne naloge.
  
  Nato sem z uporabo metode programiranja napisal programe, ki jih potrebujem za upravljanje garažnih vrat.
  
## Izbira komponent
  Ker ne potrebujem veliko precesorske moči, hkrati pa želim, da je moj projekt kar se da kompakten kot krmilnik izberem Raspberry Pi Zero W. To je najmanjša verzija Raspberry Pi-ja, z že vgrajenim WiFi-jem in Bluetoothom. Slednja bosta pri projektu najverjetneje potrebna.
  
  Za upravljanje garažnih vrat bom uporabil 1-kanalni rele. Le tega bom sprogramiral tako, da se bo obnašal kot tipka tj. zaprl se bo za kratek časovni interval prib. 0.5s, nato pa se znova odprl. Nameščen bo v bližini že obstoječe tipke, ki se uporablja za upravljanje garažnih vrat. Z le to bo vzporedno vezan.
  
  Za spremljanje stanja garažnih vrat bom uporabil reed stikala. In sicer dve stikali ter in magnet. Stikali bosta nameščeni na ogrodje vrat, medtem ko bo magnet nameščen neposredno na garažna vrata.
  
  Za spremljanje temperature v garaži uporabim 1-Wire digitalni element.... (nevem imena zle). Le ta bo nameščen nekje v garaži, po možnosti meter od tal, na najmanj prepišnem mestu v garaži.
  
  Ultrazvočni senzor, s katerim bom preverjal ali je avto v garaži ali ne, bo nameščen ali na stropbu garaže, najverjetneje pa kar na motorju garažnih vrat.
  
  Poleg že naštetih komponent bo uporabil še dve LED diodi in dve tipki. Le te bodo paroma uporabljene kot indikator stanja avta oziroma temperature v garaži. Če bo naprimer garaža odprta in bo vanjo pripeljal avto, se bo pognal program, ki bo po določenem času samodejno zaprl vrata. Istočasno, bo začela utripati ustrezna LED dioda, uporabnik pa bo imel s pritiskom tipke možnost da prekliče samodejno zapiranje garaže. Pri temperaturi je namen LED diode in tipke enak, le da spremljamo temperaturo v garaži.
  
  > vstavi sliko komponent
  
 ## Priprava Raspberry Pi-ja
 ## Priključitev komponent
 ### Rele
