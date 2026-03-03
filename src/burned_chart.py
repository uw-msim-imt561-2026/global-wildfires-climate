import pandas as pd
import plotly.express as px


def top_countries_burned_area(df: pd.DataFrame, top_n: int):
    df = df.copy()
    df["Burned_Area_Km"] = pd.to_numeric(df["Burned_Area_Km"], errors="coerce")
    df = df.dropna(subset=["Country", "Burned_Area_Km"])

    summary = (
        df.groupby("Country", as_index=False)["Burned_Area_Km"]
          .sum()
          .rename(columns={"Burned_Area_Km": "Total_Burned_Area_Km"})
          .sort_values("Total_Burned_Area_Km", ascending=False)
          .head(top_n)
    )

    fig = px.bar(
        summary,
        x="Total_Burned_Area_Km",
        y="Country",
        orientation="h",
        labels={"Total_Burned_Area_Km": "Burned Area (Km²)", "Country": "Country"},
        title=f"Top {top_n} Countries by Total Burned Area",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig, summary


def burned_area_by_region(df: pd.DataFrame, selected_country: str, top_k: int = 5):
    df = df.copy()
    df["Burned_Area_Km"] = pd.to_numeric(df["Burned_Area_Km"], errors="coerce")
    df = df.dropna(subset=["Country", "Region", "Burned_Area_Km"])

    df_c = df[df["Country"] == selected_country].copy()

    summary = (
        df_c.groupby("Region", as_index=False)["Burned_Area_Km"]
            .sum()
            .rename(columns={"Burned_Area_Km": "Total_Burned_Area_Km"})
            .sort_values("Total_Burned_Area_Km", ascending=False)
            .head(top_k)
    )

    fig = px.bar(
        summary,
        x="Total_Burned_Area_Km",
        y="Region",
        orientation="h",
        labels={"Total_Burned_Area_Km": "Burned Area (Km²)", "Region": "Region"},
        title=f"Top {top_k} Regions by Burned Area in {selected_country}",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig, summary