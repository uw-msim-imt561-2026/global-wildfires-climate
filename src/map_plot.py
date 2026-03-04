import pandas as pd
import streamlit as st
import plotly.express as px

# TODO: Add title and axes labels
def wildfire_worldmap_plot(df: pd.DataFrame, year_filter) -> None:
    filtered = df[df['Year'] == year_filter]
    fig = px.scatter_map(filtered,
                         lat='Latitude',
                         lon='Longitude',
                         color="Fires_Count",
                         size="Burned_Area_Km",
                         title="Historical Wildfire World Map",
                         color_continuous_scale="Sunsetdark",
                         hover_data=["Year", "Country", "Region"],
                         width=800,
                         height=600,
                         zoom=0.25)

    st.plotly_chart(fig)