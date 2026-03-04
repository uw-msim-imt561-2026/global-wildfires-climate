import pandas as pd
import streamlit as st

def date_slider(df: pd.DataFrame, key: str) -> str:
    # Key variable differentiates the multiple year slider widgets
    min_date = df["Year"].min()
    max_date = df["Year"].max()
    return st.slider("Select date or date-range",
                           min_value=min_date,
                           max_value=max_date,
                            key=key)

def weather_condition_select() -> str:
    cols = ["Temperature_C","Humidity_Percent","Wind_Speed_kmh"]
    return st.selectbox("Select weather condition", cols)


def country_select(df: pd.DataFrame, year_filter: str, key: str) -> list:
    year_filter = int(year_filter)
    filtered_df = df[df["Year"] == year_filter]

    countries = sorted(filtered_df["Country"].unique())

    selected_countries = st.multiselect("Select country(s)", options=countries, default=countries, key=key)

    return selected_countries