import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json

def formatNumberOfChar(code, requiredLen):
    return "0"*(requiredLen-len(code)) + str(code)

def panel(dataset):
    jsonData = open("data/communes.geojson","r")
    jsonString = jsonData.read()
    locations = json.loads(jsonString)
    jsonData.close()

    partiByCandidate = {
        "Front National" : "#0D378A",
        "En Marche" : "#ffeb00",
        "La France Insoumise" : "#cc2443",
        "Les Républicains" : "#0066CC",
        "Debout la France" : "#0082C4",
        "Parti Socialiste" : "#FF8080",
        "Nouveau Parti Anticapitaliste" : "#bb0000",
        "Lutte Ouvrière" : "#bb0000",
        "Resistons" : "#26c4ec",
        "Solidarité et Progrès" : "#dddddd",
        "Union Populaire Républicaine" : "#118088"
    }

    dataset["code_insee"] = dataset["code_insee"].apply(lambda x : formatNumberOfChar(str(x),5)) #On met au format 5 chiffres pour la liaison avec le geoJSON

    mapPanel = px.choropleth_mapbox(
        dataset,
        geojson=locations,
        featureidkey="properties.code",
        locations="code_insee", 
        mapbox_style="open-street-map",
        center={"lat": 46.227638, "lon": 2.213749},
        zoom=3,
        title="Résultats des votes à l'élections de 2017 par commune"
        )
    return mapPanel