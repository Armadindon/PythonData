import dash
import json
import os
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

def loadDept(code):
    with open(os.path.join("data", "geojsonByDpt", code ,"communes.geojson")) as f:
        result = json.load(f)
    return result

app = dash.Dash(__name__, prevent_initial_callbacks=True)

#On Load les datasets
dataset = pd.read_csv("data/votes_departements.csv")
datasetCity = pd.read_csv("data/votes_communes.csv")
baseLocations = []
with open("data/departements.geojson","r") as f:
    baseLocations = json.load(f)

locations = baseLocations.copy()
cityLocations = []

#On initialise les panels
chloropethMap = ChloroMap(dataset,datasetCity,locations,cityLocations)

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
        figure=chloropethMap.mapPanel,
    )
])

@app.callback(
    Output("electionMap", "figure"),
    [Input("electionMap","clickData")]
)
def update_map(data):
    global deptSelected
    cityLocations = []
    deptSelected = data["points"][0]["customdata"][0]
    locations = baseLocations.copy()
    print("On update la map !")
    cityLocations = loadDept(deptSelected)
    locations["features"] = list(filter(lambda x: not x["properties"]["code"] == deptSelected, locations["features"]))
    chloropethMap.update(dataset,datasetCity,locations,cityLocations)
    chloropethMap.generateMap()

    return chloropethMap.mapPanel


if __name__ == '__main__':
    app.run_server(debug=True)