import pandas as pd
import plotly.express as px
import streamlit as st

#TODO: Rename axes,
def scatter_weather_conditions_plot(df: pd.DataFrame, y_axis_column: dict, year_filter: str) -> None:
    filtered = df[df['Year'] == year_filter]

    fig = px.scatter(filtered,
                     x="Cause",
                     y=y_axis_column,
                     color="Cause",
                     size="Burned_Area_Km",
                     hover_data=["Country","Region","Year"],
                     color_discrete_sequence=px.colors.qualitative.Dark2)

    fig.update_xaxes(categoryorder='category ascending')

    st.plotly_chart(fig, width="content")

