# -*- coding: utf-8 -*-

import requests
from lxml import html
from csv import DictReader, DictWriter

def formatNumberOfChar(code, requiredLen):
    return "0"*(requiredLen-len(code)) + str(code)

if __name__ == "__main__":
    fileCommunes = open("data/communes.csv")
    communesReader = DictReader(fileCommunes)

    partiByCandidate = {
        "Mme Marine LE PEN" : ("Front National", "MLEPEN"),
        "M. Emmanuel MACRON" : ("En Marche", "EMACRON"),
        "M. Jean-Luc MÉLENCHON" : ("La France Insoumise", "JLMELENCHON"),
        "M. François FILLON" : ("Les Républicains", "FFILLON"),
        "M. Nicolas DUPONT-AIGNAN" : ("Debout la France", "NDUPONTAIGNAN"),
        "M. Benoît HAMON" : ("Parti Socialiste", "BHAMON"),
        "M. Philippe POUTOU" : ("Nouveau Parti Anticapitaliste", "PPOUTOU"),
        "Mme Nathalie ARTHAUD" : ("Lutte Ouvrière", "NARTHAUD"),
        "M. Jean LASSALLE" : ("Resistons", "JLASSALLE"),
        "M. Jacques CHEMINADE" : ("Solidarité et Progrès", "JCHEMINADE"),
        "M. François ASSELINEAU" : ("Union Populaire Républicaine", "FASSELINEAU")
    }

    results = []
    previousDept = "-1" #Permet de gérer l'affichage

    for commune in communesReader:
        if previousDept != commune["code_departement"]:
            previousDept = commune["code_departement"]
            print("On s'occupe du département:",commune["nom_departement"],end="")
        print(".", end="")
        deptDataRequest = requests.get("https://www.interieur.gouv.fr/Elections/Les-resultats/Presidentielles/elecresult__presidentielle-2017/(path)/presidentielle-2017/"+ formatNumberOfChar(commune["code_region"],3) +"/"+ formatNumberOfChar(commune["code_departement"],3) +"/"+ formatNumberOfChar(commune["code_commune_INSEE"],6) +".html")

        resultItem = {
            "code_insee" : commune["code_commune_INSEE"] ,
            "nom" : commune["nom_commune"]
        }

        treeDept = html.fromstring(deptDataRequest.content.decode("utf-8"))
        resultatsVote = treeDept.xpath('//table[@class="table table-bordered tableau-resultats-listes"][2]/tbody/tr')[1:] #On veut les résultats du second tour
        #On construit la map avec les résultats
        for resultByCandidate in resultatsVote:
            dataByCandidate = list(resultByCandidate.xpath("./td/text()"))
            resultItem["votes_" +partiByCandidate[dataByCandidate[0]][1]] = int(dataByCandidate[1].replace(" ",""))
            resultItem["pourcentage_inscrit_" +partiByCandidate[dataByCandidate[0]][1]] = float(dataByCandidate[2].replace(",","."))
            resultItem["pourcentage_exprime_" +partiByCandidate[dataByCandidate[0]][1]] = float(dataByCandidate[3].replace(",","."))
        
        results.append(resultItem)

    print("On enregistre les données")
    with open("data/votes_communes.csv","w+",newline="") as csvData:
        fields = [
        "code_insee","nom",
        "votes_MLEPEN","pourcentage_inscrit_MLEPEN","pourcentage_exprime_MLEPEN",
        "votes_EMACRON","pourcentage_inscrit_EMACRON","pourcentage_exprime_EMACRON",
        "votes_JLMELENCHON","pourcentage_inscrit_JLMELENCHON","pourcentage_exprime_JLMELENCHON",
        "votes_FFILLON","pourcentage_inscrit_FFILLON","pourcentage_exprime_FFILLON",
        "votes_NDUPONTAIGNAN","pourcentage_inscrit_NDUPONTAIGNAN","pourcentage_exprime_NDUPONTAIGNAN",
        "votes_BHAMON","pourcentage_inscrit_BHAMON","pourcentage_exprime_BHAMON",
        "votes_PPOUTOU","pourcentage_inscrit_PPOUTOU","pourcentage_exprime_PPOUTOU",
        "votes_NARTHAUD","pourcentage_inscrit_NARTHAUD","pourcentage_exprime_NARTHAUD",
        "votes_JLASSALLE","pourcentage_inscrit_JLASSALLE","pourcentage_exprime_JLASSALLE",
        "votes_JCHEMINADE","pourcentage_inscrit_JCHEMINADE","pourcentage_exprime_JCHEMINADE",
        "votes_FASSELINEAU","pourcentage_inscrit_FASSELINEAU","pourcentage_exprime_FASSELINEAU",
        ]
        writer = DictWriter(csvData, fieldnames=fields)
        
        writer.writeheader()
        writer.writerows(results)

    
    fileCommunes.close()
