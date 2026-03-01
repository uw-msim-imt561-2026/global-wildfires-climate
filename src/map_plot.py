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
                         color_continuous_scale="YlOrRd",
                         zoom=0.50)
    st.plotly_chart(fig)