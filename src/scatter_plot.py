import pandas as pd
import plotly.express as px
import streamlit as st
from src.cause_color_map_util import cause_color_map

#TODO: Rename axes,
def scatter_weather_conditions_plot(df: pd.DataFrame, y_axis_column: str, year_filter: str) -> None:
    filtered = df[df['Year'] == year_filter]
    name_map = {"Humidity_Percent": "Humidity Percent",
                "Temperature_C": "Temperature (C)",
                "Wind_Speed_kmh": "Wind Speed (km/h)"}
    palette = cause_color_map()

    fig = px.scatter(filtered,
                     x="Cause",
                     y=y_axis_column,
                     labels={"Cause": "Cause",
                             y_axis_column: name_map[y_axis_column]},
                     title="Distribution of Cause by Weather Condition",
                     color="Cause",
                     size="Burned_Area_Km",
                     hover_data=["Country","Region","Year"],
                     color_discrete_map=palette)


    fig.update_xaxes(categoryorder='category ascending')


    st.plotly_chart(fig, width="stretch")

