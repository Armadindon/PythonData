import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json

def formatNumberOfChar(code, requiredLen):
    return "0"*(requiredLen-len(code)) + str(code)

def panel(dataset):

    locations = gpd.read_file("data/departements.geojson")

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

    dataset["code_departement"] = dataset["code_departement"].apply(lambda x : formatNumberOfChar(str(x),2)) #On met au format 5 chiffres pour la liaison avec le geoJSON

    mapPanel = px.choropleth_mapbox(
        dataset,
        geojson=locations,
        color="parti_gagnant",
        color_discrete_map=partiByCandidate,
        featureidkey="properties.code",
        locations="code_departement", 
        mapbox_style="open-street-map",
        hover_name="nom_departement",
        hover_data={
            "code_departement" : False,
        },
        labels={"parti_gagnant" : "Parti en tête"},
        center={"lat": 46.227638, "lon": 2.213749},
        zoom=3,
        title="Résultats des votes à l'élections de 2017 par commune",
        )

    mapPanel.update_layout(height= 900)
    return mapPanel