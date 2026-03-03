import streamlit as st
from src.data import load_data
from src.scatter_plot import scatter_weather_conditions_plot
from src.filters import date_slider, weather_condition_select, country_select
from src.map_plot import wildfire_worldmap_plot
from src.bar_chart_occurrence import top_countries_burned_area
from src.cause_bar import cause_country_plot


def main() -> None:
    st.set_page_config(
        page_title="Global Wildfire Occurrences (1881-2025)",
        layout="wide",
    )

    st.title("Global Wildfire Occurrences (1881-2025)")
    st.caption("Historical view of wildfire occurrences in fire-prone regions")

    df = load_data("data/Forest_Fires_Dataset_Final.csv")

    t1, t2, t3 = st.tabs(["World Map", "Explore by Region", "Explore by Cause"])
    with t1:
        map_year = date_slider(df, key="map_year")

        wildfire_worldmap_plot(df, map_year)
    with t2:
        st.subheader("Top Countries by Total Burned Area")

        top_n = st.slider(
            "Top N countries",
            min_value=5,
            max_value=30,
            value=10,
            key="burned_top_n",
        )

        fig, summary = top_countries_burned_area(df, top_n)

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Show summary table"):
            st.dataframe(summary, use_container_width=True)
    with t3:

        scatter_year = date_slider(df, key="scatter_year")
        selected_condition = weather_condition_select()
        scatter_weather_conditions_plot(df, y_axis_column=selected_condition, year_filter=scatter_year)

        selected_countries = country_select(df, year_filter=scatter_year, key="cause_country_filter")
        cause_country_plot(df, year_filter=scatter_year, selected_countries=selected_countries)


if __name__ == "__main__":
    main()
