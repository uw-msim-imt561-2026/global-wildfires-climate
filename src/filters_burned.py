import streamlit as st
import pandas as pd

def sidebar_filters(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Applies sidebar filters and returns filtered df + selections.
    Assumes df already has columns: Year, Country, Burned_Area_Km, and optionally Region, Cause.
    """
    st.sidebar.header("Filters")

    # Year range
    year_min = int(df["Year"].min())
    year_max = int(df["Year"].max())
    year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max))

    # Top N
    top_n = st.sidebar.slider("Top N countries", 5, 30, 10)

    # Optional: Region
    selected_regions = None
    if "Region" in df.columns:
        use_region = st.sidebar.checkbox("Filter by Region", value=False)
        if use_region:
            regions = sorted(df["Region"].dropna().unique().tolist())
            selected_regions = st.sidebar.multiselect("Regions", regions, default=regions)

    # Optional: Cause
    selected_causes = None
    if "Cause" in df.columns:
        use_cause = st.sidebar.checkbox("Filter by Cause", value=False)
        if use_cause:
            causes = sorted(df["Cause"].dropna().unique().tolist())
            selected_causes = st.sidebar.multiselect("Causes", causes, default=causes)

    # Apply filters
    df_f = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

    if selected_regions is not None:
        df_f = df_f[df_f["Region"].isin(selected_regions)]

    if selected_causes is not None:
        df_f = df_f[df_f["Cause"].isin(selected_causes)]

    selections = {
        "year_range": year_range,
        "top_n": top_n,
        "selected_regions": selected_regions,
        "selected_causes": selected_causes,
    }

    return df_f, selections