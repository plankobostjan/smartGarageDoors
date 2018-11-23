# Hrošči (in ostale težave) pri projektu "pametna garažna vrata"

## #1 - rele ostane zaprt
Prva težava se je pojavila relativno hitro po prvih poskusih avtomatizacije garažnih vrat. In sicer je, iz neznanenga razloga (verjetno slaba povezava) rele, ki služi kot stikalo, občasno ostal zaprt. Posledica tega je bila, da se garažnih vrat ni več dalo upravljati ne s telefonom niti z običajnim stikalom v garaži.
### Rešitev #1
Težavo sem odpravil dokaj enostavno. Napisal sem program v Pythonu — [closeRelay.py](./closeRelay.py) —, ki ves čas preverja če v kakšnem stanju je rele. Če le ta ostane zaprt predolgo časa, ga program samodejno odpre.
Rešitev se je izkazala kot učinkovita, saj se težava od takrat naprej ne pojavlja več.
