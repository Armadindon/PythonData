import plotly.express as px

class VoteHistogram:

    def __init__(self, dataset, currentCity = None, currentDept = None):
        self.update(dataset, currentCity, currentDept)
    

    def update(self, dataset, currentCity = None, currentDept = None):
        self.dataset = dataset
        self.currentCity = currentCity
        self.currentDept = currentDept
        self.generateHistogram()

    def generateHistogram(self):
        if self.currentCity != None:
            line = self.dataset[self.dataset.code_insee == self.currentCity]
            nom = line.nom.item()

        elif self.currentDept != None:
            line = self.dataset[self.dataset.code_departement == self.currentDept]
            nom = line.nom_departement.item()

        else:
            return None
        
        x = ["Marine le Pen","Emmanuel Macron","Jean Luc Mélanchon","François Fillon","Nicolas Dupont Aignant",
        "Benoît Hamon","Philippe POUTOU","Nathalie Arthaud","Jean Lassalle","Jacques Cheminnades","François Asselinau"]

        y = [
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
        self.graph = px.histogram(x=x, y=y)

        self.graph.update_layout(title="Votes pour "+nom, xaxis_title_text="Candidats", yaxis_title_text="Nombre de votes")

