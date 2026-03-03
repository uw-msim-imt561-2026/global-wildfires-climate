import pandas as pd
import streamlit as st
import plotly.express as px

def cause_country_plot(df: pd.DataFrame, year_filter:str, selected_countries: list) -> None:
    year_filter = int(year_filter)

    if not selected_countries:
        filtered_df = df[df["Year"] == year_filter]
    else:
        filtered_df = df[(df["Year"] == year_filter) & (df["Country"].isin(selected_countries))]

    if filtered_df.empty:
        st.warning("No data available.")
        return

    country_cause = (filtered_df.groupby(["Country", "Cause"])["Fires_Count"].sum().reset_index())

    fig = px.bar(country_cause, x="Cause", y="Fires_Count",
                 color="Country",
                 barmode="group",
                 title=f"Wildfire Causes by Country ({year_filter})",
                 labels={"Fires_Count": "Total Fires",
                         "Cause": "Wildfire Cause"}
                 )

    st.plotly_chart(fig, use_container_width=True)