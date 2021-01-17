"""
Script contenant les classes permettant de représenter des Histogrammes
"""
import plotly.express as px


class VotePie:
    """
    Objet représentant un diagramme en camember
     de résultats d'élections. (Pourcentages de votes)
    """

    def __init__(self, dataset, current_city=None, current_dept=None):
        self.graph = None
        self.update(dataset, current_city, current_dept)

    def update(self, dataset, current_city=None, current_dept=None):
        """
        Permet de mette à jour les données d'un objet

        Args:
            dataset (TextFileReader): Dataset des données de l'élection
            current_city (str): Ville à afficher
            current_dept (str): Département à afficher
        """
        self.dataset = dataset
        self.current_city = current_city
        self.current_dept = current_dept
        self.generate_pie()

    def generate_pie(self):
        """
        Genère ou regenère le diagramme
        """
        if self.current_city is not None:
            line = self.dataset[self.dataset.code_insee == self.current_city]
            nom = line.nom.item()

        elif self.current_dept is not None:
            line = self.dataset[self.dataset.code_departement ==
                                self.current_dept]
            nom = line.nom_departement.item()

        else:
            return

        axis_x = ["Marine le Pen", "Emmanuel Macron", "Jean Luc Mélanchon",
                  "François Fillon", "Nicolas Dupont Aignant",
                  "Benoît Hamon", "Philippe POUTOU", "Nathalie Arthaud",
                  "Jean Lassalle", "Jacques Cheminnades", "François Asselinau"]

        axis_y = [
            line.pourcentage_exprime_MLEPEN.item(),
            line.pourcentage_exprime_EMACRON.item(),
            line.pourcentage_exprime_JLMELENCHON.item(),
            line.pourcentage_exprime_FFILLON.item(),
            line.pourcentage_exprime_NDUPONTAIGNAN.item(),
            line.pourcentage_exprime_BHAMON.item(),
            line.pourcentage_exprime_PPOUTOU.item(),
            line.pourcentage_exprime_NARTHAUD.item(),
            line.pourcentage_exprime_JLASSALLE.item(),
            line.pourcentage_exprime_JCHEMINADE.item(),
            line.pourcentage_exprime_FASSELINEAU.item(),

        ]
        self.graph = px.pie(names=axis_x, values=axis_y)

        self.graph.update_layout(title="Pourcentage des votes exprimes par candidats pour "+nom,
                                 xaxis_title_text="Candidats",
                                 yaxis_title_text="Pourcentage de votes")
