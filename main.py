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
from panels.histogram import VoteHistogram, WealthHistogram

def toLength(code, expectedLength):
    return "0"*(expectedLength-len(code)) + str(code)

def loadDept(code):
    with open(os.path.join("data", "geojsonByDpt", code ,"communes.geojson")) as f:
        result = json.load(f)
    return result

def generateSynthesis(datasetVoteDept, datasetVoteCity, datasetWealthDept, datasetWealthCity):
    cityDataset = pd.merge(datasetVoteCity, datasetWealthCity, left_on="code_insee", right_on="code_ville")
    deptDataset = pd.merge(datasetVoteDept, datasetWealthDept, on="code_departement")

    #On met en relation le revenu fiscal de référence et le parti gagnant pour les villes
    partisCity = cityDataset.parti_gagnant.unique()
    resultCity = []
    for parti in partisCity:
        resultCity.append(cityDataset[cityDataset.parti_gagnant == parti].revFiscalRefFoyers.mean())
    print(partisCity)
    print(resultCity)

    graphCity = px.histogram(x=partisCity,y=resultCity)
    
    #On fait pareil pour les departements
    partisDept = deptDataset.parti_gagnant.unique()
    resultDept = []
    for parti in partisDept:
        resultDept.append(deptDataset[deptDataset.parti_gagnant == parti].revFiscalRefFoyers.mean())

    print(resultDept)
    
    graphDepts = px.histogram(x=partisDept,y=resultDept)


    return [
        html.P("Afin de mettre en place une conclusion à cette étude,"+
        " il faut mettre en relation les données des votes avec celles des revenus fiscaux des différentes villes"),
        dcc.Graph(figure=graphCity),
        dcc.Graph(figure=graphDepts)
    ]
    

app = dash.Dash(__name__, prevent_initial_callbacks=True)

#On Load les datasets
dataset = pd.read_csv("data/votes_departements.csv", dtype={"code_departement" : str})
datasetCity = pd.read_csv("data/votes_communes.csv", dtype={"code_insee" : str})

datasetWealth = pd.read_csv("data/revenuFiscauxDepts.csv", dtype={"code_departement" : str, "revFiscalRefFoyers" : float})
datasetWealthCity = pd.read_csv("data/revenuFiscauxCommunes.csv", dtype={"code_ville" : str, "revFiscalRefFoyers" : float})

baseLocations = []
with open("data/departements.geojson","r") as f:
    baseLocations = json.load(f)

locations = baseLocations.copy()
cityLocations = []

#On initialise les panels
chloropethMap = ChloroMap(dataset,datasetCity,locations,cityLocations)
deptVoteHistogram = VoteHistogram(dataset)
cityVoteHistogram = VoteHistogram(datasetCity)
deptWealthHistogram = WealthHistogram(datasetWealth)
cityWealthHistogram = WealthHistogram(datasetWealthCity)

#On gère les callbacks
deptSelected = "-1"
citySelected = "-1"

app.layout = html.Div(id="body", children=[
    html.Div(id="navbar",children=[
        html.Ul(id="links", children=[
            html.Li("Carte de France", className="selected" , id="cdf-button"),
            html.Li("Info du département" , id="idd-button", className="hide"),
            html.Li("Info de la ville", id="idv-button", className="hide"),
            html.Li("Synthèse de l'analyse", id="synth-button")
        ])
    ]),

    html.Div(id="App", children=[dcc.Graph(id="electionMap",figure=chloropethMap.mapPanel)])
])


@app.callback(
    [Output("electionMap", "figure"), Output("links", "children")],
    [Input("electionMap","clickData")]
)
def update_map(data):
    global deptSelected
    links = [html.Li("Carte de France", className="selected" , id="cdf-button"),]
    cityLocations = []
    if len(data["points"][0]["customdata"][0]) == 2 :
        deptSelected = data["points"][0]["customdata"][0]

        #On update l'histogramme
        deptVoteHistogram.update(dataset,currentDept=deptSelected)
        deptWealthHistogram.update(datasetWealth, currentDept=deptSelected)

        #On Update la map
        locations = baseLocations.copy()
        cityLocations = loadDept(deptSelected)
        locations["features"] = list(filter(lambda x: not x["properties"]["code"] == deptSelected, locations["features"]))
        chloropethMap.update(dataset,datasetCity,locations,cityLocations)
        chloropethMap.generateMap()

        #On Update les liens
        links.append(html.Li("Info du département" , id="idd-button"))
        links.append(html.Li("Info de la ville", id="idv-button", className="hide"))

    else:
        citySelected = data["points"][0]["customdata"][0]

        #On update l'histogramme
        cityVoteHistogram.update(datasetCity,currentCity=citySelected)
        cityWealthHistogram.update(datasetWealthCity, currentCity=citySelected)

        #On ajoute les liens
        links.append(html.Li("Info du département" , id="idd-button"))
        links.append(html.Li("Info de la ville", id="idv-button"))
    
    links.append(html.Li("Synthèse de l'analyse", id="synth-button"))

    return (chloropethMap.mapPanel, links)


@app.callback(
    [
        Output("App","children"),
        Output("cdf-button","className"),
        Output("idd-button","className"),
        Output("idv-button","className"),
        Output("synth-button","className"),
    ],
    [
        Input("cdf-button","n_clicks"),
        Input("idd-button","n_clicks"),
        Input("idv-button","n_clicks"),
        Input("synth-button","n_clicks")
    ]
)
def changeTab(n1 ,n2 ,n3, n4):
    srcInput = dash.callback_context.triggered[0]["prop_id"]

    if "cdf-button" in srcInput:
        return ([
            dcc.Graph(id="electionMap",figure=chloropethMap.mapPanel)
            ], "selected", "", "", "")
    elif "idd-button" in srcInput:
        return ([
            html.H1("Résultats par candidat"),
            dcc.Graph(figure=deptVoteHistogram.graph),
            html.H1("Données économiques"),
            dcc.Graph(figure=deptWealthHistogram.graph)
            ], "", "selected", "", "")
    elif "idv-button" in srcInput:
        return ([
            html.H1("Résultats par candidat"),
            dcc.Graph(figure=cityVoteHistogram.graph),
            html.H1("Données économiques"),
            dcc.Graph(figure=cityWealthHistogram.graph)
             ], "", "", "selected", "")
    
    elif "synth-button" in srcInput:
        return (generateSynthesis(dataset,datasetCity, datasetWealth, datasetWealthCity), "", "", "", "selected")


if __name__ == '__main__':
    app.run_server(debug=True)