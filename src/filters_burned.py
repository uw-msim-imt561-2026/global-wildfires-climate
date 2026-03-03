import pandas as pd
import streamlit as st


def burned_area_controls(top_country_df: pd.DataFrame) -> str:
    if "Country" not in top_country_df.columns or top_country_df.empty:
        st.error("No countries available to choose from.")
        st.stop()

    countries = top_country_df["Country"].dropna().astype(str).tolist()

    selected_country = st.selectbox(
        "Choose a country (from Top N) to see its regions",
        options=countries,
        key="burned_selected_country",
    )

    return selected_country