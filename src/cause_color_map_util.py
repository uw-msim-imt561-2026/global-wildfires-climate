import plotly.express as px

def cause_color_map() -> dict:
    palette = px.colors.qualitative.Bold
    print(palette)
    return {
        "Climate Change": palette[0],
        "Deforestation": palette[1],
        "Human": palette[2],
        "Lightning": palette[3],
        "Unknown": palette[4]
    }