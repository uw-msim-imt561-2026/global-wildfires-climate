import streamlit as st
from src.data import load_data
from src.scatter_plot import scatter_weather_conditions_plot
from src.filters import date_slider, weather_condition_select


def main() -> None:
    st.set_page_config(
        page_title="Global Wildfire Occurrences (1881-2025)",
        layout="wide",
    )

    st.title("Global Wildfire Occurrences (1881-2025)")
    st.caption("Historical view of wildfire occurrences in fire-prone regions")

    df = load_data("data/Forest_Fires_Dataset_Final.csv")

    selected_year = date_slider(df)
    selected_condition = weather_condition_select()

    scatter_weather_conditions_plot(df, y_axis_column=selected_condition, year_filter=selected_year)


if __name__ == "__main__":
    main()
