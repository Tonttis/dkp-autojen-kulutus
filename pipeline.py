"""Lataa ja siivoa auton kulutusdata sekä tallentaa sen SQLiteen."""

from io import StringIO
import pandas as pd
import requests
from database import save_cars

# Auto MPG (UCI), CSV-versio seaborn-data-projektissa.
DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"


def read_data():
    """Hae CSV-tiedosto internetistä."""
    response = requests.get(DATA_URL, timeout=20)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text))


def clean_data(df):
    """Siivoa dataa ja lisää kaksi laskettua saraketta."""
    df = df.copy()
    df = df.drop_duplicates()

    # Korjataan tekstien ylimääräiset välilyönnit.
    df["name"] = df["name"].astype("string").str.strip()
    df["origin"] = df["origin"].astype("string").str.strip().str.lower()

    # Jos hevosvoimia puuttuu, ne saa jättää tyhjiksi.
    df["horsepower"] = pd.to_numeric(df["horsepower"], errors="coerce")
    df["mpg"] = pd.to_numeric(df["mpg"], errors="coerce")
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")
    df["model_year"] = pd.to_numeric(df["model_year"], errors="coerce")

    # Pudotetaan vain rivit, joita ei voida käyttää kaaviossa.
    df = df.dropna(subset=["name", "origin", "mpg", "weight", "model_year"])
    df = df[df["mpg"] > 0].copy()

    # USA:n mpg -> litraa / 100 km, paunat -> kilogrammat.
    df["l_100km"] = (235.214583 / df["mpg"]).round(2)
    df["weight_kg"] = (df["weight"] * 0.45359237).round(0)
    df["year"] = df["model_year"].astype(int) + 1900

    return df


def main():
    print("Ladataan Auto MPG -aineisto...")
    try:
        original = read_data()
    except requests.RequestException as error:
        print("Lataus ei onnistunut:", error)
        return

    print("Alkuperäisiä rivejä:", len(original))
    print("Puuttuvia hevosvoima-arvoja:", original["horsepower"].isna().sum())

    cleaned = clean_data(original)
    save_cars(cleaned)
    print("Tietokantaan tallennettuja autoja:", len(cleaned))
    print("Valmis! Käynnistä seuraavaksi Streamlit.")


if __name__ == "__main__":
    main()
