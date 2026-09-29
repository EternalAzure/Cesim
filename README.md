# Graafisia analyysejä

Ohjelma lukee excel tiedostoja ja luo niiden tiedoista python objecteja analyysiä varten.

Main functio luo ```Product``` olioita jotka se syöttää ```Market``` olioon, jonka se syöttää ```Analyse``` olioon. Oliot sisältävät vain yksin kertaisia työkaluja tiedon käsittelyyn.

Ohjelman kiinnostavin osuus on Analyse luokka joka piirtää kaavioita käyttäen ```matplotlib``` -kirjastoa. Luokkaa kutsutaan main-moduulin main-funktiossa.

Käyttöohje:<br>
Ohjelmalla ei ole käyttöliittymää ja sitä ajetaan vain muokkaamalla koodia.<br>

Kuinka valita Excel:<br>
```book = xlrd.open_workbook("/home/miisu/Desktop/repos/cesim/src/cesim/results-r03.xls")``` 

Kuinka ajaa ohjelma:<br>
```uv run cesim```

Kuinka valita kaavio:<br>
aja koodin pätkiä main funktiossa.<br>
```
# -- ALOITA TÄSTÄ -- #
# 1) Löydä suosituimmat tyylit
#analyse_europe.design()
```