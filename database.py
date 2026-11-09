"""SQLite-tietokannan tallennus ja lukeminen."""

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent / "data" / "autot.db"


def save_cars(df):
    """Luo kaksi taulua ja korvaa niiden sisältö puhdistetulla datalla."""
    DB_PATH.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute("""
            CREATE TABLE IF NOT EXISTS origins (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                year INTEGER NOT NULL,
                cylinders INTEGER,
                horsepower REAL,
                mpg REAL NOT NULL,
                l_100km REAL NOT NULL,
                weight_kg REAL NOT NULL,
                origin_id INTEGER NOT NULL,
                FOREIGN KEY (origin_id) REFERENCES origins(id)
            )
        """)

        # Tyhjennetään vanhat tiedot, jotta uusi ajo ei tee tuplia.
        connection.execute("DELETE FROM cars")
        connection.execute("DELETE FROM origins")

        for origin in sorted(df["origin"].unique()):
            connection.execute("INSERT INTO origins (name) VALUES (?)", (str(origin),))

        origins = dict(connection.execute("SELECT name, id FROM origins").fetchall())

        for _, row in df.iterrows():
            horsepower = None if pd.isna(row["horsepower"]) else float(row["horsepower"])
            connection.execute("""
                INSERT INTO cars
                    (name, year, cylinders, horsepower, mpg, l_100km, weight_kg, origin_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(row["name"]),
                int(row["year"]),
                int(row["cylinders"]),
                horsepower,
                float(row["mpg"]),
                float(row["l_100km"]),
                float(row["weight_kg"]),
                origins[str(row["origin"])],
            ))


def get_cars():
    """Hae visualisoinnissa tarvittavat tiedot kahdesta taulusta."""
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query("""
            SELECT cars.name, cars.year, cars.cylinders, cars.horsepower,
                   cars.mpg, cars.l_100km, cars.weight_kg,
                   origins.name AS origin
            FROM cars
            JOIN origins ON cars.origin_id = origins.id
            ORDER BY cars.year, cars.name
        """, connection)
