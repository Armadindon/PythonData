# -*- coding: utf-8 -*-
"""
Script permettant l'obtention de données de l'elections de 2017
à partir du site de gouvernement:
https://www.interieur.gouv.fr/Elections/Les-resultats/Presidentielles/elecresult__presidentielle-2017/
"""
import os
from csv import DictReader, DictWriter
import requests
from lxml import html


def format_number_of_char(code, required_len):
    """
    Fonction utilitaire afin de mettre une chaine de caractères à
    la longueur souhaitée en ajoutant des '0' avant
    """
    return "0"*(required_len-len(code)) + str(code)


def main():
    """
    Fonction Principale
    """
    file_communes = open(os.path.join('data', 'communes.csv'))
    communes_reader = DictReader(file_communes)

    fields = [
        "code_insee", "nom", "parti_gagnant",
        "votes_MLEPEN",
        "pourcentage_inscrit_MLEPEN", "pourcentage_exprime_MLEPEN",
        "votes_EMACRON",
        "pourcentage_inscrit_EMACRON", "pourcentage_exprime_EMACRON",
        "votes_JLMELENCHON",
        "pourcentage_inscrit_JLMELENCHON", "pourcentage_exprime_JLMELENCHON",
        "votes_FFILLON",
        "pourcentage_inscrit_FFILLON", "pourcentage_exprime_FFILLON",
        "votes_NDUPONTAIGNAN",
        "pourcentage_inscrit_NDUPONTAIGNAN", "pourcentage_exprime_NDUPONTAIGNAN",
        "votes_BHAMON",
        "pourcentage_inscrit_BHAMON", "pourcentage_exprime_BHAMON",
        "votes_PPOUTOU",
        "pourcentage_inscrit_PPOUTOU", "pourcentage_exprime_PPOUTOU",
        "votes_NARTHAUD",
        "pourcentage_inscrit_NARTHAUD", "pourcentage_exprime_NARTHAUD",
        "votes_JLASSALLE",
        "pourcentage_inscrit_JLASSALLE", "pourcentage_exprime_JLASSALLE",
        "votes_JCHEMINADE",
        "pourcentage_inscrit_JCHEMINADE", "pourcentage_exprime_JCHEMINADE",
        "votes_FASSELINEAU",
        "pourcentage_inscrit_FASSELINEAU", "pourcentage_exprime_FASSELINEAU",
    ]

    parti_by_candidate = {
        "Mme Marine LE PEN": ("Front National", "MLEPEN"),
        "M. Emmanuel MACRON": ("En Marche", "EMACRON"),
        "M. Jean-Luc MÉLENCHON": ("La France Insoumise", "JLMELENCHON"),
        "M. François FILLON": ("Les Républicains", "FFILLON"),
        "M. Nicolas DUPONT-AIGNAN": ("Debout la France", "NDUPONTAIGNAN"),
        "M. Benoît HAMON": ("Parti Socialiste", "BHAMON"),
        "M. Philippe POUTOU": ("Nouveau Parti Anticapitaliste", "PPOUTOU"),
        "Mme Nathalie ARTHAUD": ("Lutte Ouvrière", "NARTHAUD"),
        "M. Jean LASSALLE": ("Resistons", "JLASSALLE"),
        "M. Jacques CHEMINADE": ("Solidarité et Progrès", "JCHEMINADE"),
        "M. François ASSELINEAU": ("Union Populaire Républicaine", "FASSELINEAU")
    }

    results = []
    previous_dept = "-1"  # Permet de gérer l'affichage

    for commune in communes_reader:
        if previous_dept != commune["code_departement"]:
            previous_dept = commune["code_departement"]
            print("On s'occupe du département:", commune["nom_departement"])
        dept_data_request = requests.get("https://www.interieur.gouv.fr/" +
                                       "Elections/Les-resultats/"+
                                       "Presidentielles/elecresult__presidentielle-2017/" +
                                       "(path)/presidentielle-2017/" +
                                       format_number_of_char(commune["code_region"], 3) + "/" +
                                       format_number_of_char(commune["code_departement"], 3) + "/" +
                                       format_number_of_char(commune["code_commune_INSEE"], 6)
                                       + ".html")

        result_item = {
            "code_insee": commune["code_commune_INSEE"],
            "nom": commune["nom_commune"]
        }

        # On veut les résultats du second tour
        resultats_vote = html.fromstring(dept_data_request.content.decode("utf-8")
        ).xpath('//table[@class="table' +
                ' table-bordered tableau-resultats-listes"][2]/tbody/tr')
        parti_gagnant = ("", -1)
        # On construit la map avec les résultats
        for result_by_candidate in resultats_vote:
            data_by_candidate = list(result_by_candidate.xpath("./td/text()"))

            if parti_gagnant[1] < int(data_by_candidate[1].replace(" ", "")):
                parti_gagnant = (parti_by_candidate[data_by_candidate[0]][0],
                                int(data_by_candidate[1].replace(" ", "")))

            result_item["votes_" + parti_by_candidate[data_by_candidate[0]]
                       [1]] = int(data_by_candidate[1].replace(" ", ""))
            result_item["pourcentage_inscrit_" + parti_by_candidate[data_by_candidate[0]]
                       [1]] = float(data_by_candidate[2].replace(",", "."))
            result_item["pourcentage_exprime_" + parti_by_candidate[data_by_candidate[0]]
                       [1]] = float(data_by_candidate[3].replace(",", "."))

        result_item["parti_gagnant"] = parti_gagnant[0]

        if not all(x in result_item.keys() for x in fields):
            print("Problèmes de données !", result_item,)
            print("Il manque", list(
                filter(lambda x: x not in result_item.keys(), fields)), "\n")
            continue

        results.append(result_item)

    print("On enregistre les données")
    with open(os.path.join('data', 'votes_communes.csv'),
    "w+", newline="", encoding='utf-8') as csv_data:

        writer = DictWriter(csv_data, fieldnames=fields)

        writer.writeheader()
        writer.writerows(results)

    file_communes.close()


if __name__ == "__main__":
    main()
