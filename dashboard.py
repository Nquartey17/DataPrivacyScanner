from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

def init_dashboard(server):

    df = pd.DataFrame({
        "Category": ["Low", "Medium", "High"],
        "Count": [10,25,7]
    })

    fig = px.bar(
        df,
        x="Category",
        y="Count",
        title="Privacy Risks"
    )

    dash_app = Dash(__name__,server=server,routes_pathname_prefix="/dashboard/")

    dash_app.layout = html.Div([
        html.H1("Sample Dashboard"),

        dcc.Graph(figure=fig)
    ])

    return dash_app