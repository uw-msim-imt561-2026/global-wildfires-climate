import streamlit as st
from src.data import load_data
from src.scatter_plot import scatter_weather_conditions_plot
from src.filters import date_slider, weather_condition_select
from src.map_plot import wildfire_worldmap_plot


def main() -> None:
    st.set_page_config(
        page_title="Global Wildfire Occurrences (1881-2025)",
        layout="wide",
    )

    st.title("Global Wildfire Occurrences (1881-2025)")
    st.caption("Historical view of wildfire occurrences in fire-prone regions")

    df = load_data("data/Forest_Fires_Dataset_Final.csv")

    with st.container():
        map_year = date_slider(df, key="map_year")

        wildfire_worldmap_plot(df, map_year)

    with st.container():
        scatter_year = date_slider(df, key="scatter_year")
        selected_condition = weather_condition_select()

        scatter_weather_conditions_plot(df, y_axis_column=selected_condition, year_filter=scatter_year)


if __name__ == "__main__":
    main()
