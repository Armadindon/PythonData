import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

#panels import
from panels.electionMap import ChloroMap

def toLength(code, expectedLength):
    return "0"*(expectedLength-len(code)) + str(code)

app = dash.Dash(__name__)

dataset = pd.read_csv("data/votes_departements.csv")
locations = []
with open("data/departements.geojson","r") as f:
    locations = json.load(f)


#On initialise les panels
chloropethMap = ChloroMap(dataset,locations)

#On gère les callbacks
deptSelected = "-1"

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.P(id='placeholder'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    
    dcc.Graph(
        id="electionMap",
        figure=chloropethMap.mapPanel
        )

])

@app.callback(
    Output("placeholder", "children"),
    [Input("electionMap","clickData")]
)
def update_map(data):
    global deptSelected
    print(deptSelected, data["points"][0]["customdata"][0])
    
    if deptSelected == data["points"][0]["customdata"][0]:
        print("On update la map !")

    deptSelected = data["points"][0]["customdata"][0]


if __name__ == '__main__':
    app.run_server(debug=True)