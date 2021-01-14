"""
Script d'installation du projet:
Fait :          -Installation des dépendances
                -Formatte les fichiers de la manière nécéssaires

Ne Fait Pas :   -Installe les dépendances pip
                -Fait le café
"""
import sys
import time
from dataScripts import (add_to_communes,
get_election_data, get_election_data_by_dept, simplify_geojson, xls_files_to_csv)


if __name__ == "__main__":

    print("===Lancement du programme d'installation des dépendances===")
    full = "--full" in sys.argv or "-f" in sys.argv

    print("On ajoute les communes 'manquantes'")
    add_to_communes.main()

    if full: #En clonant le repository git, cette étape n'est pas nécéssaire
        print("ATTENTION : Cette partie risque de prendre beaucoup de temps ! (jusqu'a 12h)")
        print("Ne perdez pas la connexion, ou ne mettez pas fin à ce script durant cette"+
        " période\n\n")

        print("On récupère les données de vote par ville\n")
        time.sleep(2) #On met un peu de temps afin que l'on puisse lire le programme
        get_election_data.main()

        print("On récupère les données de vote par départements\n")
        time.sleep(2) #On met un peu de temps afin que l'on puisse lire le programme
        get_election_data_by_dept.main()

    print("On formate les geojson comme nécéssaire")
    simplify_geojson.main()

    print("On récupère les données du xls pour les mettres en csv")
    xls_files_to_csv.main()

    print("===Fin du programme d'installation des dépendances===")
