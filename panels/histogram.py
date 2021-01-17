"""
Script contenant les classes permettant de représenter des Histogrammes
"""
import plotly.express as px


class VoteHistogram:
    """
    Objet représentant un histogramme de résultats d'élections. (Votes par candidats)
    """

    def __init__(self, dataset, current_city=None, current_dept=None):
        self.graph = None
        self.update(dataset, current_city, current_dept)

    def update(self, dataset, current_city=None, current_dept=None):
        """
        Met à jour les données de l'objet

        Args:
            dataset (TextFileReader): Dataset des données de l'élection
            current_city (str): Ville à afficher
            current_dept (str): Département à afficher
        """
        self.dataset = dataset
        self.current_city = current_city
        self.current_dept = current_dept
        self.generate_histogram()

    def generate_histogram(self):
        """
        Genère l'histogramme à partir des données
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
            line.votes_MLEPEN.item(),
            line.votes_EMACRON.item(),
            line.votes_JLMELENCHON.item(),
            line.votes_FFILLON.item(),
            line.votes_NDUPONTAIGNAN.item(),
            line.votes_BHAMON.item(),
            line.votes_PPOUTOU.item(),
            line.votes_NARTHAUD.item(),
            line.votes_JLASSALLE.item(),
            line.votes_JCHEMINADE.item(),
            line.votes_FASSELINEAU.item(),

        ]
        self.graph = px.histogram(x=axis_x, y=axis_y)

        self.graph.update_layout(
            title="Votes pour "+nom,
            xaxis_title_text="Candidats",
            yaxis_title_text="Nombre de votes")
