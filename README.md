# Autojen kulutus – yksinkertainen dataputki

Xamk, tehtävä 6. Pythonilla tehty harjoitus, jossa tutkitaan vanhojen autojen polttoaineenkulutusta.

## Datalähde

- Alkuperäinen: [UCI Auto MPG](https://archive.ics.uci.edu/dataset/9/auto+mpg), R. Quinlan (1993), CC BY 4.0.
- Käytetty CSV-versio: [seaborn-data/mpg.csv](https://github.com/mwaskom/seaborn-data/blob/master/mpg.csv).
- Aineisto koostuu autoista vuosilta 1970–1982. Kulutus on aluksi USA:n mpg-yksikössä.

## Projektin tiedostot

- `pipeline.py`: lataa aineiston, poistaa duplikaatit, käsittelee puuttuvat arvot ja laskee uudet sarakkeet.
- `database.py`: luo SQLite-tietokannan sekä tallentaa ja lukee tiedot.
- `app.py`: näyttää SQLite-tietokannasta haetut tiedot Streamlitissä.
- `requirements.txt`: Python-kirjastot.
- `data/autot.db`: syntyy automaattisesti dataputkea suorittaessa (ei mukana GitHubissa).

## Käynnistäminen Windowsissa (PowerShell)

Avaa terminaali projektin juurikansiossa:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe pipeline.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Selaimessa avautuu yleensä `http://localhost:8501`.

Jos ajat dataputken uudelleen, SQLite-tietokannan vanhat autorivit korvataan uusilla. Näin samat tiedot eivät kerry moneen kertaan.

## Taulut ja niiden suhde

`origins` sisältää alkuperäalueiden nimet. `cars` sisältää autot, ja jokaisella autolla on `origin_id`, joka viittaa `origins.id`-sarakkeeseen.

```text
origins                           cars
--------------------              ------------------------------
id (PRIMARY KEY)     <----------- origin_id (FOREIGN KEY)
name (UNIQUE)                     id (PRIMARY KEY)
                                  name, year, mpg, l_100km, ...
```

Tämä on yhden suhde moneen -rakenne: samalla alkuperäalueella voi olla monta autoa.

## Puhdistus ja laskenta

- Poistetaan täsmälleen samanlaiset duplikaattirivit. Sama mallinimi eri vuosilta voi jäädä aineistoon.
- Korjataan tekstien ympäriltä välilyönnit.
- Muutetaan numeeriset sarakkeet numeroiksi. Puuttuvat hevosvoimat säilytetään tyhjinä, jotta muut auton tiedot eivät katoa.
- Uudet arvot: `l_100km = 235.214583 / mpg` ja `weight_kg = weight * 0.45359237`.
- Mallivuosien `70–82` arvot muutetaan vuosiksi `1970–1982`.

## Huomioita

Aineisto on historiallinen ja sisältää puuttuvia hevosvoimatietoja. Se sopii harjoitteluun, mutta siitä ei voi päätellä suoraan nykyautojen kulutusta tai mikä muuttuja yksin aiheuttaa kulutuksen muutoksia.

Tiedot haetaan internetistä `pipeline.py`-komennolla. Streamlit lukee vain paikallista SQLite-tietokantaa, ei suoraan verkosta.
