"""
Script contenant les classes permettant de représenter des cartes
"""
import plotly.express as px


def format_number_of_char(code, required_len):
    """
    Fonction utilitaire afin de mettre une chaine de caractères à
    la longueur souhaitée en ajoutant des '0' avant
    """
    return "0"*(required_len-len(code)) + str(code)


class ChloroMap:
    """
    Objet représentant une carte de résultats d'élections.
    Elle a 2 couches : une pour les départements et une pour les villes
    """
    def __init__(self, dataset, dataset_by_city, locations, city_locations):
        self.update(dataset, dataset_by_city, locations, city_locations)
        self.generate_map()

    def generate_map(self):
        """
        Permet de générer ou regéner la map en fonction des données
        de l'objet
        """
        parti_by_candidate = {
            "En Marche": "#ffeb00",
            "Front National": "#0D378A",
            "La France Insoumise": "#cc2443",
            "Les Républicains": "#0066CC",
            "Debout la France": "#0082C4",
            "Parti Socialiste": "#FF8080",
            "Nouveau Parti Anticapitaliste": "#bb0000",
            "Lutte Ouvrière": "#bb0000",
            "Resistons": "#26c4ec",
            "Solidarité et Progrès": "#dddddd",
            "Union Populaire Républicaine": "#118088"
        }

        self.map_panel = px.choropleth_mapbox(
            self.dataset,
            geojson=self.locations,
            color="parti_gagnant",
            color_discrete_map=parti_by_candidate,
            featureidkey="properties.code",
            locations="code_departement",
            mapbox_style="open-street-map",
            hover_name="nom_departement",
            hover_data={
                "code_departement": False,
            },
            labels={"parti_gagnant": "Parti en tête"},
            center={"lat": 46.227638, "lon": 2.213749},
            zoom=3,
            title="Résultats des votes à l'élections de 2017 par commune",
            height=900,
        )

        if len(self.city_locations) != 0:
            layer = px.choropleth_mapbox(
                self.dataset_by_city,
                geojson=self.city_locations,
                color="parti_gagnant",
                color_discrete_map=parti_by_candidate,
                featureidkey="properties.code",
                locations="code_insee",
                mapbox_style="open-street-map",
                hover_name="nom",
                center={"lat": 46.227638, "lon": 2.213749},
                zoom=3,
                hover_data={
                    "code_insee": False,
                },
                labels={"parti_gagnant": "Parti en tête"},
                height=900
            )

            for data in layer.data:
                self.map_panel.add_trace(
                    data
                )

        self.map_panel.update_layout(clickmode="event")

    def update(self, dataset, dataset_by_city, locations, city_locations):
        """
        Permet de mettre à jour les données de l'objet
        """
        self.dataset = dataset
        self.dataset_by_city = dataset_by_city
        self.locations = locations
        self.city_locations = city_locations
        # On met au format 2 chiffres pour la liaison avec le geoJSON
        self.dataset["code_departement"] = self.dataset["code_departement"].apply(
            lambda x: format_number_of_char(str(x), 2))
            # On met au format 5 chiffres pour la liaison avec le geoJSON
        self.dataset_by_city["code_insee"] = self.dataset_by_city["code_insee"].apply(
            lambda x: format_number_of_char(str(x), 5))
