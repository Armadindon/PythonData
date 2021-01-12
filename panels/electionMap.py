import plotly.express as px

def formatNumberOfChar(code, requiredLen):
    return "0"*(requiredLen-len(code)) + str(code)

class ChloroMap:

    def __init__(self, dataset, datasetByCity, locations, cityLocations):
        self.update(dataset, datasetByCity, locations, cityLocations)
        self.generateMap()

    def generateMap(self):

        partiByCandidate = {
            "En Marche" : "#ffeb00",
            "Front National" : "#0D378A",
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
            
        self.mapPanel = px.choropleth_mapbox(
            self.dataset,
            geojson=self.locations,
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
            height=900,
            )
        
        if len(self.cityLocations) != 0:
            layer = px.choropleth_mapbox(
                    self.datasetByCity,
                    geojson=self.cityLocations,
                    color="parti_gagnant",
                    color_discrete_map=partiByCandidate,
                    featureidkey="properties.code",
                    locations="code_insee", 
                    mapbox_style="open-street-map",
                    hover_name="nom",
                    center={"lat": 46.227638, "lon": 2.213749},
                    zoom=3,
                    hover_data={
                        "code_insee" : False,
                    },
                    labels={"parti_gagnant" : "Parti en tête"},
                    height=900
                )
            
            for data in layer.data:
                self.mapPanel.add_trace(
                    data
                )

        self.mapPanel.update_layout(clickmode="event")

    def update(self, dataset, datasetByCity, locations, cityLocations):
        self.dataset = dataset
        self.datasetByCity = datasetByCity
        self.locations = locations
        self.cityLocations = cityLocations
        self.dataset["code_departement"] = self.dataset["code_departement"].apply(lambda x : formatNumberOfChar(str(x),2)) #On met au format 2 chiffres pour la liaison avec le geoJSON
        self.datasetByCity["code_insee"] = self.datasetByCity["code_insee"].apply(lambda x : formatNumberOfChar(str(x),5)) #On met au format 5 chiffres pour la liaison avec le geoJSON
