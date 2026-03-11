import streamlit as st
from src.data import load_data
from src.scatter_plot import scatter_weather_conditions_plot
from src.filters import sidebar_filters, weather_condition_select
from src.line_charts import total_fires_trend, comparative_trend
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
    # Apply filters
    year_range, selected_countries, selected_causes = sidebar_filters(df)

    start_year, end_year = year_range
    df_filtered = df[
        (df["Year"] >= start_year) &
        (df["Year"] <= end_year) &
        (df["Country"].isin(selected_countries)) &
        (df["Cause"].isin(selected_causes))
        ]


    with st.container():
        st.markdown("#### 🔥Key Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Burned Area (Km2)", df_filtered["Burned_Area_Km"].sum().round(0).astype(int))
        with col2:
            st.metric('Top Cause', df_filtered['Cause'].mode()[0] if not df_filtered.empty else "N/A")
        with col3:
            subcol1, subcol2, subcol3 = st.columns(3)
            with subcol1:
                mean_temp = df_filtered['Temperature_C'].mean().round(2) if not df_filtered.empty else 0
                st.metric('Temp (C)', mean_temp)
            with subcol2:
                mean_wind_speed = df_filtered['Wind_Speed_kmh'].mean().round(2) if not df_filtered.empty else 0
                st.metric('Wind Speed (km/h)', mean_wind_speed)
            with subcol3:
                mean_humidity = df_filtered['Humidity_Percent'].mean().round(2) if not df_filtered.empty else 0
                st.metric('Humidity', mean_humidity)

    st.divider()

    t1, t2, t3, t4 = st.tabs(["Explore World Map", "Explore Trend", "Explore by Region", "Explore by Cause"])
    with t1:
        st.subheader("Wildfire Hotspots on the World Map")
        wildfire_worldmap_plot(df_filtered, year_range)

    with t2:
        st.subheader("Wildfire Trend Analysis")
        total_fires_trend(df_filtered, year_range)

        st.markdown("---")
        comparison_type = st.radio(
            "Compare Trend By:",
            options=["Top 5 Countries", "Causes"]
        )

        comparative_trend(df_filtered, comparison_type=comparison_type, top_n=5, year_range=year_range)

    with t3:
        st.subheader("Top Countries & Regional Breakdown (Burned Area)")
        if df_filtered.empty:
            st.warning("No Data Available")

        # Top N countries
        max_count = len(df_filtered['Country'].unique())
        top_n = st.slider("Top N Countries", 0, max_count, value=max_count, key="burned_top_n") if max_count > 0 else 0
        fig_c, top_countries_df = top_countries_burned_area(df_filtered, top_n, year_range)
        st.plotly_chart(fig_c, width='stretch')

        # Pick a country from the Top N list (via your filters module)
        selected_country = burned_area_controls(top_countries_df)

        # Top K regions within that country
        top_k = st.slider(
            "Top K Regions (within selected country)",
            0, 3, 3,
            key="burned_top_k_regions"
        )

        fig_r, region_df = burned_area_by_region(df_filtered, selected_country, top_k=top_k)
        st.plotly_chart(fig_r, width='stretch')

        with st.expander("Show tables"):
            st.write("Top Countries")
            st.dataframe(top_countries_df, width='stretch')
            st.write(f"Top {top_k} Regions in {selected_country}")
            st.dataframe(region_df, width='stretch')
    with t4:
        st.subheader("Distribution of Cause by Country and Weather Conditions")
        with st.container():
            cause_country_plot(df_filtered, year_range)
        with st.container():
            selected_condition = weather_condition_select()
            scatter_weather_conditions_plot(df_filtered, y_axis_column=selected_condition, year_range=year_range)


if __name__ == "__main__":
    main()
