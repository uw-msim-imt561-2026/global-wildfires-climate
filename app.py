import streamlit as st
from src.data import load_data
from src.scatter_plot import scatter_weather_conditions_plot
from src.filters import date_slider, weather_condition_select, country_select
from src.map_plot import wildfire_worldmap_plot
from src.burned_chart import top_countries_burned_area, burned_area_by_region
from src.filters_burned import burned_area_controls
from src.cause_bar import cause_country_plot

def main() -> None:
    st.set_page_config(
        page_title="Global Wildfire Occurrences (1881-2025)",
        layout="wide",
    )

    st.title("Global Wildfire Occurrences (1881-2025)")
    st.subheader("Historical view of wildfire occurrences in fire-prone regions")
    st.caption("Reference: uw-msim-imt561-2026/global-wildfires-climate")

    df = load_data("data/Forest_Fires_Dataset_Final.csv")

    t1, t2, t3 = st.tabs(["Explore World Map", "Explore by Region", "Explore by Cause"])
    with t1:
        map_year = date_slider(df, key="map_year")
        wildfire_worldmap_plot(df, map_year)

    with t2:
        st.subheader("Top Countries & Regional Breakdown (Burned Area)")

        # Top N countries
        top_n = st.slider("Top N Countries", 5, 30, 10, key="burned_top_n")
        fig_c, top_countries_df = top_countries_burned_area(df, top_n)
        st.plotly_chart(fig_c, width='stretch')

        # Pick a country from the Top N list (via your filters module)
        selected_country = burned_area_controls(top_countries_df)

        # Top K regions within that country
        top_k = st.slider(
            "Top K Regions (within selected country)",
            3, 20, 5,
            key="burned_top_k_regions"
        )

        fig_r, region_df = burned_area_by_region(df, selected_country, top_k=top_k)
        st.plotly_chart(fig_r, width='stretch')

        with st.expander("Show tables"):
            st.write("Top Countries")
            st.dataframe(top_countries_df, width='stretch')
            st.write(f"Top {top_k} Regions in {selected_country}")
            st.dataframe(region_df, width='stretch')
    with t3:
        st.subheader("Distribution of Cause by Country and Weather Conditions")
        with st.container():
            country_cause_year = date_slider(df, key="country_cause_year")
            selected_countries = country_select(df, year_filter=country_cause_year, key="cause_country_filter")
            cause_country_plot(df, year_filter=country_cause_year, selected_countries=selected_countries)
        with st.container():
            scatter_year = date_slider(df, key="scatter_year")
            selected_condition = weather_condition_select()
            scatter_weather_conditions_plot(df, y_axis_column=selected_condition, year_filter=scatter_year)


if __name__ == "__main__":
    main()
