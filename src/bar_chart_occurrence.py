import pandas as pd
import plotly.express as px

def top_countries_burned_area(df: pd.DataFrame, top_n: int) -> tuple:
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
        title=f"Top {top_n} Countries by Total Burned Area",
        labels={"Total_Burned_Area_Km": "Total Burned Area (Km²)", "Country": "Country"},
    )


    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    return fig, summary