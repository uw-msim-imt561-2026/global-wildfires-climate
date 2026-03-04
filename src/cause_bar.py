import pandas as pd
import streamlit as st
import plotly.express as px
from src.cause_color_map_util import cause_color_map

def cause_country_plot(df: pd.DataFrame, year_filter:str, selected_countries: list) -> None:
    year_filter = int(year_filter)

    filtered_df = df[df["Year"] == year_filter]

    if selected_countries:
        filtered_df = filtered_df[
            filtered_df["Country"].isin(selected_countries)
        ]

    if filtered_df.empty:
        st.warning("No data available.")
        return

    country_cause = (filtered_df.groupby(["Country", "Cause"])["Fires_Count"].sum().reset_index())

    fig = px.bar(country_cause, x="Country", y="Fires_Count",
                 color="Cause",
                 barmode="group",
                 title=f"Wildfire Causes by Country ({year_filter})",
                 labels={"Fires_Count": "Total Fires",
                         "Country": "Country",
                         "Cause": "Wildfire Cause"},
                 color_discrete_map=cause_color_map()
                 )
    fig.update_layout(xaxis_tickangle=0)

    st.plotly_chart(fig, width='stretch')