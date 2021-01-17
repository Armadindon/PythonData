"""
Fichier principal, contient toute la partie propre au fonctionnel de
l'application et du serveur.
"""
import os
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# panels import
from panels.election_map import ChloroMap
from panels.histogram import VoteHistogram
from panels.pie import VotePie


def to_length(code, expected_length):
    """
    Fonction utilitaire afin de mettre une chaine de caractères à
    la longueur souhaitée en ajoutant des '0' avant.

    Args:
        code (str): Chaine de caractères à modifier.

        expected_length (int): Entier représentant la longueur souhaité.

    Returns:
        str:Chaine de caractères modifié.
    """
    return "0"*(expected_length-len(code)) + str(code)


def load_dept(code):
    """
    Charge le geojson d'un departement et renvoie les villes de ce departement.

    Args:
        code (str): Chaine de caractères qui représente le code du département.

    Returns:
        result(obj): Objet python contenant les villes du département.
    """
    with open(os.path.join("data", "geojsonByDpt", code, "communes.geojson")) as file:
        result = json.load(file)
    return result


def generate_economic_report(dataset, code_dept=None, code_city=None):
    """
    Genère un "rapport économique" (présentant les différentes données que l'on a pour cet endroit)
    Que l'on peut afficher dans les onglets.

    Args:
        dataset (TextFileReader): Set qui contient les données économiques.
        code_dept (str): Chaine de caractère qui represente le code du département.
        code_city (str): Chaine de caractère qui respresente le code de la commune.

    Returns:
        html.Div: Div html pour le module dash qui represente le rapport économique de l'endroit
    """
    if code_dept is not None:
        line = dataset[dataset.code_departement == code_dept]

    elif code_city is not None:
        line = dataset[dataset.code_ville == code_city]

    else:
        return None

    return html.Div([
        html.P("Pour cet endroit, nous avons ces données :",
               className="boldFront"),
        html.P(
            [html.Span(f"{int(line.nbFoyerFiscaux.item())}",
                       className="boldFront"), " foyers fiscaux"]
            if line.nbFoyerFiscaux.item() is not None
            else "Pas de données pour les foyers fiscaux"
        ),
        html.P(
            ["Revenu fiscal de référence des foyers fiscaux : ", html.Span(
                f"{int(line.revFiscalRefFoyers.item())} euros", className="boldFront")]
            if line.revFiscalRefFoyers.item() is not None
            else "Pas de données pour le revenu fiscal de référence des foyers fiscaux"
        ),
        html.P(
            ["Total des impôts nets : ", html.Span(
                f"{int(line.impotNet.item())} euros", className="boldFront")]
            if line.impotNet.item() is not None
            else "Pas de données pour l'impot net"
        ),
        html.P(
            [html.Span(f"{int(line.nbFoyersImposes.item())}",
                       className="boldFront"), " foyers fiscaux imposes"]
            if line.nbFoyersImposes.item() is not None
            else "Pas de données pour les foyers fiscaux imposes"
        ),
        html.P(
            ["Revenu fiscal de référence des foyers fiscaux imposes : ", html.Span(
                f"{int(line.nbFoyerFiscaux.item())} euros", className="boldFront")]
            if line.nbFoyerFiscaux.item() is not None
            else "Pas de données pour le revenu fiscal de référence des foyers fiscaux imposes"
        ),
    ])


def generate_synthesis(dataset_vote_dept,
                       dataset_vote_city, dataset_wealth_dept, dataset_wealth_city):
    """
    Genère le contenu de l'onglet synthèse.

    Args:
        dataset_vote_dept (TextFileReader): Set qui contient la répartition des votes du département
        dataset_vote_city (TextFileReader): Set qui contient la répartition des votes de la commune
        dataset_wealth_dept (TextFileReader): Set qui contient les données économiques du département
        dataset_wealth_city (TextFileReader): Set qui contient les données économiques de la commune
    """
    city_dataset = pd.merge(dataset_vote_city, dataset_wealth_city,
                            left_on="code_insee", right_on="code_ville")
    dept_dataset = pd.merge(
        dataset_vote_dept, dataset_wealth_dept, on="code_departement")

    # On ajoute les colonnes "Pourcentage imposables"
    city_dataset["percentImposable"] = city_dataset.apply(
        lambda x: x["nbFoyersImposes"] / x["nbFoyerFiscaux"] * 100
        if x["nbFoyerFiscaux"] != 0
        and x["nbFoyersImposes"] is not None
        and x["nbFoyerFiscaux"] is not None
        else None, axis=1)

    dept_dataset["percentImposable"] = dept_dataset.apply(
        lambda x: x["nbFoyersImposes"] / x["nbFoyerFiscaux"] * 100
        if x["nbFoyerFiscaux"] != 0
        and x["nbFoyersImposes"] is not None
        and x["nbFoyerFiscaux"] is not None
        else None, axis=1)

    # On met en relation le pourcentage de personnes imposables et le parti gagnant pour les villes
    partis_city = city_dataset.parti_gagnant.unique()
    result_city = []
    for parti in partis_city:
        result_city.append(
            city_dataset[city_dataset.parti_gagnant == parti].percentImposable.mean())

    graph_city = px.histogram(x=partis_city, y=result_city)
    graph_city.update_layout(title="Pourcentage de foyers imposables" +
                             " moyen par rapport au parti gagnant",
                             xaxis_title_text="Parti Gagnants",
                             yaxis_title_text="Pourcentage de foyers imposables")

    # On fait pareil pour les departements
    partis_dept = dept_dataset.parti_gagnant.unique()
    result_dept = []
    for parti in partis_dept:
        result_dept.append(
            dept_dataset[dept_dataset.parti_gagnant == parti].percentImposable.mean())

    graph_depts = px.histogram(x=partis_dept, y=result_dept)
    graph_depts.update_layout(title="Pourcentage de foyers imposables" +
                              " moyen par rapport au parti gagnant",
                              xaxis_title_text="Parti Gagnants",
                              yaxis_title_text="Pourcentage de foyers imposables")

    return [
        html.P("Afin de mettre en place une conclusion à cette étude," +
               " il faut mettre en relation les données des " +
               "votes avec celles des revenus fiscaux des différentes villes"),
        html.H1("Données pour les villes"),
        dcc.Graph(figure=graph_city),
        html.H1("Données pour les Départements"),
        dcc.Graph(figure=graph_depts)
    ]


dash_app = dash.Dash(__name__, prevent_initial_callbacks=True)
app = dash_app.server

# On Load les datasets

vote_dataset_dept = pd.read_csv(os.path.join("data", "votes_departements.csv"), dtype={
    "code_departement": str})
vote_dataset_city = pd.read_csv(os.path.join(
    "data", "votes_communes.csv"), dtype={"code_insee": str})

wealth_dataset_depts = pd.read_csv(os.path.join("data", "revenuFiscauxDepts.csv"), dtype={
    "code_departement": str, "revFiscalRefFoyers": float})
wealth_dataset_city = pd.read_csv(os.path.join("data", "revenuFiscauxCommunes.csv"), dtype={
    "code_ville": str, "revFiscalRefFoyers": float})

base_locations = []
with open(os.path.join("data", "departements.geojson"), "r") as f:
    base_locations = json.load(f)

locations = base_locations.copy()
city_locations = []

# On initialise les panels
chloropeth_map = ChloroMap(
    vote_dataset_dept, vote_dataset_city, locations, city_locations)
vote_histogram_dept = VoteHistogram(vote_dataset_dept)
vote_histogram_city = VoteHistogram(vote_dataset_city)
vote_pie_dept = VotePie(vote_dataset_dept)
vote_pie_city = VotePie(vote_dataset_city)

# On gère les callbacks
selected_dept = "-1"
selected_city = "-1"

dash_app.layout = html.Div(id="body", children=[
    html.Div(id="navbar", children=[
        html.Ul(id="links", children=[
            html.Li("Carte de France", className="selected", id="cdf-button"),
            html.Li("Info du département", id="idd-button", className="hide"),
            html.Li("Info de la ville", id="idv-button", className="hide"),
            html.Li("Synthèse de l'analyse", id="synth-button")
        ])
    ]),

    html.Div(id="App", children=[dcc.Graph(
        id="electionMap", figure=chloropeth_map.map_panel)])
])


@dash_app.callback(
    [Output("electionMap", "figure"), Output("links", "children")],
    [Input("electionMap", "clickData")]
)
def update_map(data):
    """
    Callback mettant à jour la map après un click sur un département ou une ville
    """
    global selected_dept, selected_city
    links = [html.Li("Carte de France", className="selected",
                     id="cdf-button"), ]
    city_locations = []

    if data is not None and len(data["points"][0]["customdata"][0]) == 2:
        selected_dept = data["points"][0]["customdata"][0]

        # On update les graphs
        vote_histogram_dept.update(
            vote_dataset_dept, current_dept=selected_dept)
        vote_pie_dept.update(vote_dataset_dept, current_dept=selected_dept)

        # On Update la map
        locations = base_locations.copy()
        city_locations = load_dept(selected_dept)
        locations["features"] = list(filter(
            lambda x: not x["properties"]["code"] == selected_dept, locations["features"]))
        chloropeth_map.update(
            vote_dataset_dept, vote_dataset_city, locations, city_locations)
        chloropeth_map.generate_map()

    elif data is not None:
        selected_city = data["points"][0]["customdata"][0]

        # On update l'histogramme
        vote_histogram_city.update(
            vote_dataset_city, current_city=selected_city)
        vote_pie_city.update(vote_dataset_city, current_city=selected_city)

    # On met à jour les liens
    if selected_dept != "-1":
        links.append(html.Li("Info du département", id="idd-button"))
    else:
        links.append(html.Li("Info du département",
                             id="idd-button", className="hide"))

    if selected_city != "-1":
        links.append(html.Li("Info de la ville", id="idv-button"))
    else:
        links.append(html.Li("Info de la ville",
                             id="idv-button", className="hide"))

    links.append(html.Li("Synthèse de l'analyse", id="synth-button"))

    return (chloropeth_map.map_panel, links)


@dash_app.callback(
    [
        Output("App", "children"),
        Output("cdf-button", "className"),
        Output("idd-button", "className"),
        Output("idv-button", "className"),
        Output("synth-button", "className"),
    ],
    [
        Input("cdf-button", "n_clicks"),
        Input("idd-button", "n_clicks"),
        Input("idv-button", "n_clicks"),
        Input("synth-button", "n_clicks")
    ]
)
def change_tab(_n_clicks_1, _n_clicks_2, _n_clicks_3, _n_clicks_4):
    """
    Permet de changer d'onglet en cas de clics sur le menu
    """
    global selected_dept, selected_city
    src_input = dash.callback_context.triggered[0]["prop_id"]

    if "cdf-button" in src_input:
        return ([
            dcc.Graph(id="electionMap", figure=chloropeth_map.map_panel)
        ],
            "selected",
            "" if selected_dept != "-1" else "hide",
            "" if selected_city != "-1" else "hide",
            ""
        )

    if "idd-button" in src_input:
        return ([
            html.H1("Résultats par candidat"),
            dcc.Graph(figure=vote_histogram_dept.graph),
            dcc.Graph(figure=vote_pie_dept.graph),
            html.H1("Données économiques"),
            generate_economic_report(
                wealth_dataset_depts, code_dept=selected_dept)
        ],
            "",
            "selected",
            "" if selected_city != "-1" else "hide",
            ""
        )

    if "idv-button" in src_input:
        return ([
            html.H1("Résultats par candidat"),
            dcc.Graph(figure=vote_histogram_city.graph),
            dcc.Graph(figure=vote_pie_city.graph),
            html.H1("Données économiques"),
            generate_economic_report(
                wealth_dataset_city, code_city=selected_city)
        ],
            "",
            "",
            "selected",
            ""
        )

    if "synth-button" in src_input:
        return (generate_synthesis(vote_dataset_dept,
                                   vote_dataset_city, wealth_dataset_depts,
                                   wealth_dataset_city),
                "",
                "" if selected_dept != "-1" else "hide",
                "" if selected_city != "-1" else "hide",
                "selected"
                )

    return None

if __name__ == '__main__':
    dash_app.run_server(debug=True)
