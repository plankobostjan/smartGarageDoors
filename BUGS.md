# Hrošči (in ostale težave) pri projektu "pametna garažna vrata"

## Kazalo vsebine
<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Hrošči (in ostale težave) pri projektu "pametna garažna vrata"](#hroi-in-ostale-teave-pri-projektu-pametna-garana-vrata)
	- [Kazalo vsebine](#kazalo-vsebine)
	- [#1 - rele ostane zaprt](#1-rele-ostane-zaprt)
		- [Rešitev #1](#reitev-1)
	- [#2 - geslo shranjeno kot tekst](#2-geslo-shranjeno-kot-tekst)
		- [Rešitev #2](#reitev-2)
	- [#3 - dnevnik dogodkov [izboljšava]](#3-dnevnik-dogodkov-izboljava)

<!-- /TOC -->

## #1 - rele ostane zaprt
Prva težava se je pojavila relativno hitro po prvih poskusih avtomatizacije garažnih vrat. In sicer je, iz neznanenga razloga (verjetno slaba povezava) rele, ki služi kot stikalo, občasno ostal zaprt. Posledica tega je bila, da se garažnih vrat ni več dalo upravljati ne s telefonom niti z običajnim stikalom v garaži.
### Rešitev #1
Težavo sem odpravil dokaj enostavno. Napisal sem program v Pythonu — [closeRelay.py](./closeRelay.py) —, ki ves čas preverja v kakšnem stanju je rele. Če le ta ostane zaprt predolgo časa, ga program samodejno odpre.
Rešitev se je izkazala kot učinkovita, saj se težava od takrat naprej ne pojavlja več.

## #2 - geslo shranjeno kot tekst
Trenutno je geslo za Raspberry Pi v [garage.sh](./garage.sh) shranjeno kot tekst. To predstavlja varnostno luknjo, zato moram čim prej najti rešitev.
### Rešitev #2
Z malce brskanja po spletu sem relativno hitro našel [rešitev](https://serverfault.com/questions/241588/how-to-automate-ssh-login-with-password). Sicer sem o uporabi ključev razmišljal že prej, zdaj pa sem ugotovil, da je to najlažja rešitev.

Kot sem že omenil zgoraj, sem težavo rešil z uporabo SSH ključa brez gesla. Ključ sem generiral na telefonu, nato pa ga kopiral na Raspberry Pi.

```BASH
$ ssh-keygen -t rsa -b 2048 #generiramo ključ
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/username/.ssh/id_rsa.
Your public key has been saved in /home/username/.ssh/id_rsa.pub.

$ ssh-copy-id user@server #kopiramo ključ na strežnik (Raspberry Pi)
user@server password:
```

Zdaj se je mogoče prijaviti v strežnik brez uporabe gesla.

## #3 - dnevnik dogodkov [izboljšava]
Mislim, da nebi bila slaba ideja, če bi se vsi dogodki na strežniku beležili v dnevniško datoteko.
Da bi to realiziral, je potrebno implementirati pisanje dnevniške datoteke v vse programe, ki se uporabljajo.
