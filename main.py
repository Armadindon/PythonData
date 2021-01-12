import dash
import json
import os
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

#panels import
from panels.electionMap import ChloroMap
from panels.histogram import VoteHistogram
from panels.pie import VotePie

def toLength(code, expectedLength):
    return "0"*(expectedLength-len(code)) + str(code)

def loadDept(code):
    with open(os.path.join("data", "geojsonByDpt", code ,"communes.geojson")) as f:
        result = json.load(f)
    return result

def generateEconomicReport(dataset, codeDept = None, codeCity = None):
    
    if codeDept != None:
        line = dataset[dataset.code_departement == codeDept]
    
    elif codeCity != None:
        line = dataset[dataset.code_ville == codeCity]
    
    else:
        return None
    
    return html.Div([
        html.P(f"Pour cet endroit, nous avons ces données :", className="boldFront"),
        html.P(
            [html.Span(f"{int(line.nbFoyerFiscaux.item())}", className="boldFront")," foyers fiscaux"] 
            if line.nbFoyerFiscaux.item() != None else "Pas de données pour les foyers fiscaux"
            ),
        html.P(
            ["Revenu fiscal de référence des foyers fiscaux : ", html.Span(f"{int(line.revFiscalRefFoyers.item())} euros", className="boldFront")] 
            if line.revFiscalRefFoyers.item() != None else "Pas de données pour le revenu fiscal de référence des foyers fiscaux"
            ),
        html.P(
            ["Total des impôts nets : ", html.Span(f"{int(line.impotNet.item())} euros", className="boldFront")]
            if line.impotNet.item() != None else "Pas de données pour l'impot net"
            ),
        html.P(
            [html.Span(f"{int(line.nbFoyersImposes.item())}", className="boldFront"), " foyers fiscaux imposes"]
            if line.nbFoyersImposes.item() != None else "Pas de données pour les foyers fiscaux imposes"
            ),
        html.P(
            ["Revenu fiscal de référence des foyers fiscaux imposes : ", html.Span(f"{int(line.nbFoyerFiscaux.item())} euros", className="boldFront")] 
            if line.nbFoyerFiscaux.item() != None else "Pas de données pour le revenu fiscal de référence des foyers fiscaux imposes"
            ),
    ])

def generateSynthesis(datasetVoteDept, datasetVoteCity, datasetWealthDept, datasetWealthCity):
    cityDataset = pd.merge(datasetVoteCity, datasetWealthCity, left_on="code_insee", right_on="code_ville")
    deptDataset = pd.merge(datasetVoteDept, datasetWealthDept, on="code_departement")

    #On ajoute les colonnes "Pourcentage imposables"
    cityDataset["percentImposable"] = cityDataset.apply(
        lambda x: x["nbFoyersImposes"] / x["nbFoyerFiscaux"] * 100
        if x["nbFoyerFiscaux"] != 0 and x["nbFoyersImposes"] != None and x["nbFoyerFiscaux"] != None else None
        , axis=1)
    
    deptDataset["percentImposable"] = deptDataset.apply(
        lambda x: x["nbFoyersImposes"] / x["nbFoyerFiscaux"] * 100
        if x["nbFoyerFiscaux"] != 0 and x["nbFoyersImposes"] != None and x["nbFoyerFiscaux"] != None else None
        , axis=1)

    #On met en relation le pourcentage de personnes imposables et le parti gagnant pour les villes
    partisCity = cityDataset.parti_gagnant.unique()
    resultCity = []
    for parti in partisCity:
        resultCity.append(cityDataset[cityDataset.parti_gagnant == parti].percentImposable.mean())

    graphCity = px.histogram(x=partisCity,y=resultCity)
    graphCity.update_layout(title="Pourcentage de foyers imposables moyen par rapport au parti gagnant", 
    xaxis_title_text="Parti Gagnants", yaxis_title_text="Pourcentage de foyers imposables")

    
    #On fait pareil pour les departements
    partisDept = deptDataset.parti_gagnant.unique()
    resultDept = []
    for parti in partisDept:
        resultDept.append(deptDataset[deptDataset.parti_gagnant == parti].percentImposable.mean())
    
    graphDepts = px.histogram(x=partisDept,y=resultDept)
    graphDepts.update_layout(title="Pourcentage de foyers imposables moyen par rapport au parti gagnant", 
    xaxis_title_text="Parti Gagnants", yaxis_title_text="Pourcentage de foyers imposables")


    return [
        html.P("Afin de mettre en place une conclusion à cette étude,"+
        " il faut mettre en relation les données des votes avec celles des revenus fiscaux des différentes villes"),
        html.H1("Données pour les villes"),
        dcc.Graph(figure=graphCity),
        html.H1("Données pour les Départements"),
        dcc.Graph(figure=graphDepts)
    ]
    

dash_app = dash.Dash(__name__, prevent_initial_callbacks=True)
app = dash_app.server

#On Load les datasets

dataset = pd.read_csv(os.path.join("data","votes_departements.csv"), dtype={"code_departement" : str})
datasetCity = pd.read_csv(os.path.join("data","votes_communes.csv"), dtype={"code_insee" : str})

datasetWealth = pd.read_csv(os.path.join("data","revenuFiscauxDepts.csv"), dtype={"code_departement" : str, "revFiscalRefFoyers" : float})
datasetWealthCity = pd.read_csv(os.path.join("data","revenuFiscauxCommunes.csv"), dtype={"code_ville" : str, "revFiscalRefFoyers" : float})

baseLocations = []
with open(os.path.join("data","departements.geojson"),"r") as f:
    baseLocations = json.load(f)

locations = baseLocations.copy()
cityLocations = []

#On initialise les panels
chloropethMap = ChloroMap(dataset,datasetCity,locations,cityLocations)
deptVoteHistogram = VoteHistogram(dataset)
cityVoteHistogram = VoteHistogram(datasetCity)
deptVotePie = VotePie(dataset)
cityVotePie = VotePie(datasetCity)

#On gère les callbacks
deptSelected = "-1"
citySelected = "-1"

dash_app.layout = html.Div(id="body", children=[
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


@dash_app.callback(
    [Output("electionMap", "figure"), Output("links", "children")],
    [Input("electionMap","clickData")]
)
def update_map(data):
    global deptSelected, citySelected
    links = [html.Li("Carte de France", className="selected" , id="cdf-button"),]
    cityLocations = []
    
    if data != None and len(data["points"][0]["customdata"][0]) == 2:
        deptSelected = data["points"][0]["customdata"][0]

        #On update les graphs
        deptVoteHistogram.update(dataset,currentDept=deptSelected)
        deptVotePie.update(dataset,currentDept=deptSelected)

        #On Update la map
        locations = baseLocations.copy()
        cityLocations = loadDept(deptSelected)
        locations["features"] = list(filter(lambda x: not x["properties"]["code"] == deptSelected, locations["features"]))
        chloropethMap.update(dataset,datasetCity,locations,cityLocations)
        chloropethMap.generateMap()


    elif data != None:
        citySelected = data["points"][0]["customdata"][0]

        #On update l'histogramme
        cityVoteHistogram.update(datasetCity,currentCity=citySelected)
        cityVotePie.update(datasetCity,currentCity=citySelected)

    #On met à jour les liens
    if deptSelected != "-1":
        links.append(html.Li("Info du département" , id="idd-button"))
    else:
        links.append(html.Li("Info du département" , id="idd-button", className="hide"))

    if citySelected != "-1":
        links.append(html.Li("Info de la ville", id="idv-button"))
    else:
        links.append(html.Li("Info de la ville", id="idv-button", className="hide"))
    
    links.append(html.Li("Synthèse de l'analyse", id="synth-button"))

    return (chloropethMap.mapPanel, links)


@dash_app.callback(
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
    global deptSelected, citySelected
    srcInput = dash.callback_context.triggered[0]["prop_id"]

    if "cdf-button" in srcInput:
        return ([
            dcc.Graph(id="electionMap",figure=chloropethMap.mapPanel)
            ], 
            "selected", 
            "" if deptSelected != "-1" else "hide", 
            "" if citySelected != "-1" else "hide", 
            ""
            )
    elif "idd-button" in srcInput:
        return ([
            html.H1("Résultats par candidat"),
            dcc.Graph(figure=deptVoteHistogram.graph),
            dcc.Graph(figure=deptVotePie.graph),
            html.H1("Données économiques"),
            generateEconomicReport(datasetWealth,codeDept=deptSelected)
            ], 
            "", 
            "selected", 
            "" if citySelected != "-1" else "hide", 
            ""
            )
    elif "idv-button" in srcInput:
        return ([
            html.H1("Résultats par candidat"),
            dcc.Graph(figure=cityVoteHistogram.graph),
            dcc.Graph(figure=cityVotePie.graph),
            html.H1("Données économiques"),
            generateEconomicReport(datasetWealthCity,codeCity=citySelected)
             ], 
            "", 
            "",
            "selected", 
            ""
            )
    
    elif "synth-button" in srcInput:
        return (generateSynthesis(dataset,datasetCity, datasetWealth, datasetWealthCity),
        "",
        "" if deptSelected != "-1" else "hide", 
        "" if citySelected != "-1" else "hide", 
        "selected"
        )


if __name__ == '__main__':
    dash_app.run_server(debug=True)