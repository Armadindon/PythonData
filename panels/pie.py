import plotly.express as px
import plotly

class VotePie:

    def __init__(self, dataset, currentCity = None, currentDept = None):
        self.update(dataset, currentCity, currentDept)
    

    def update(self, dataset, currentCity = None, currentDept = None):
        self.dataset = dataset
        self.currentCity = currentCity
        self.currentDept = currentDept
        self.generatePie()

    def generatePie(self):
        if self.currentCity != None:
            line = self.dataset[self.dataset.code_insee == self.currentCity]
            nom = line.nom.item()

        elif self.currentDept != None:
            line = self.dataset[self.dataset.code_departement == self.currentDept]
            nom = line.nom_departement.item()

        else:
            return None

        colorByCandidate = {
            "Emmanuel Macron" : "#ffeb00",
            "Marine le Pen" : "#0D378A",
            "Jean Luc Mélanchon" : "#cc2443",
            "François Fillon" : "#0066CC",
            "Nicolas Dupont Aignant" : "#0082C4",
            "Benoît Hamon" : "#FF8080",
            "Philippe POUTOU" : "#bb0000",
            "Nathalie Arthaud" : "#bb0000",
            "Jean Lassalle" : "#26c4ec",
            "Jacques Cheminnades" : "#dddddd",
            "François Asselinau" : "#118088"
        }
        
        x = ["Marine le Pen","Emmanuel Macron","Jean Luc Mélanchon","François Fillon","Nicolas Dupont Aignant",
        "Benoît Hamon","Philippe POUTOU","Nathalie Arthaud","Jean Lassalle","Jacques Cheminnades","François Asselinau"]

        y = [
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
        self.graph = px.pie(names=x, values=y, color_discrete_map=colorByCandidate)

        self.graph.update_layout(title="Pourcentage des votes exprimes par candidats pour "+nom, xaxis_title_text="Candidats", yaxis_title_text="Pourcentage de votes")