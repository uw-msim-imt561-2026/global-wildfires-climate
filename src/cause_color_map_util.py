import plotly.express as px

def cause_color_map() -> dict:
    palette = px.colors.qualitative.Bold
    return {
        "Climate Change": "#1e1a75",
        "Deforestation": "#a11477",
        "Human": "#e13661",
        "Lightning": "#ff6f4b",
        "Unknown": "#ffa951"
    }