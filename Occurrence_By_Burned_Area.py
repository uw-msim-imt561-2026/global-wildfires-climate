import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Top Countries by Burned Area", layout="wide")
st.title("Top Countries by Total Burned Area")
st.caption("Interactive bar chart. Hover to see totals. Use filters in the sidebar.")

CSV_PATH = "data/Forest_Fires_Dataset_Enhancedcopy.csv"

#Load
df = pd.read_csv(CSV_PATH)

#Clean required columns
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Burned_Area_Km"] = pd.to_numeric(df["Burned_Area_Km"], errors="coerce")

df = df.dropna(subset=["Country", "Year", "Burned_Area_Km"]).copy()
df["Year"] = df["Year"].astype(int)

#Sidebar filters
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

with st.sidebar:
    st.header("Filters")
    year_range = st.slider("Year range", min_year, max_year, (min_year, max_year))
    top_n = st.slider("Top N countries", 5, 30, 10)

    # Filter by region
    use_region = st.checkbox("Filter by Region", value=False)
    if use_region and "Region" in df.columns:
        regions = sorted(df["Region"].dropna().unique().tolist())
        selected_regions = st.multiselect("Regions", regions, default=regions)
    else:
        selected_regions = None
    # Filter by cause
    use_cause = st.checkbox("Filter by Cause", value=False)
    if use_cause and "Cause" in df.columns:
        causes = sorted(df["Cause"].dropna().unique().tolist())
        selected_causes = st.multiselect("Causes", causes, default=causes)
    else:
        selected_causes = None

# Apply filters
df_f = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

if selected_regions is not None:
    df_f = df_f[df_f["Region"].isin(selected_regions)]

if selected_causes is not None:
    df_f = df_f[df_f["Cause"].isin(selected_causes)]

# Aggregate: total burned area per country
summary = (
    df_f.groupby("Country", as_index=False)["Burned_Area_Km"]
        .sum()
        .rename(columns={"Burned_Area_Km": "Total_Burned_Area_Km"})
        .sort_values("Total_Burned_Area_Km", ascending=False)
        .head(top_n)
)

# interactive bar chart
fig = px.bar(
    summary,
    x="Total_Burned_Area_Km",
    y="Country",
    orientation="h",
    title=f"Top {top_n} Countries by Total Burned Area ({year_range[0]}–{year_range[1]})",
    labels={"Total_Burned_Area_Km": "Total Burned Area (Km²)", "Country": "Country"},
)

# Show largest at top
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

# Show table
with st.expander("Show table"):
    st.dataframe(summary, use_container_width=True)