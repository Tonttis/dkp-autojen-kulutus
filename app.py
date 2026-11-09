"""Autojen kulutuksen yksinkertainen Streamlit-näkymä."""

import streamlit as st
from database import DB_PATH, get_cars

st.set_page_config(page_title="Autojen kulutus", page_icon="🚗")
st.title("Autojen kulutus 1970–1982")
st.write("Tutki vanhojen autojen polttoaineenkulutusta.")

if not DB_PATH.exists():
    st.warning("Tietokantaa ei vielä ole. Suorita ensin: python pipeline.py")
    st.stop()

cars = get_cars()
if cars.empty:
    st.warning("Tietokannassa ei ole autoja.")
    st.stop()

# Rajataan käyttäjän valitsemiin tietoihin.
all_origins = sorted(cars["origin"].unique())
selected_origins = st.multiselect("Valitse alkuperä", all_origins, default=all_origins)
min_year = int(cars["year"].min())
max_year = int(cars["year"].max())
selected_years = st.slider("Vuosimallit", min_year, max_year, (min_year, max_year))

filtered = cars[
    cars["origin"].isin(selected_origins)
    & cars["year"].between(selected_years[0], selected_years[1])
]

if filtered.empty:
    st.info("Näillä valinnoilla ei löytynyt autoja.")
    st.stop()

st.write("Autoja valinnassa:", len(filtered))
st.write("Keskimääräinen kulutus:", round(filtered["l_100km"].mean(), 1), "l/100 km")

st.subheader("Keskikulutus vuosittain")
yearly = filtered.groupby("year")["l_100km"].mean()
st.line_chart(yearly)

st.subheader("Auton paino ja kulutus")
st.scatter_chart(filtered, x="weight_kg", y="l_100km")

st.subheader("Autot taulukkona")
st.dataframe(
    filtered[["name", "year", "origin", "cylinders", "horsepower", "weight_kg", "l_100km"]],
    use_container_width=True,
)

st.caption("Lähde: UCI Auto MPG (seaborn-data CSV). Kyseessä on historiallinen aineisto, ei nykyautojen testituloksia.")
