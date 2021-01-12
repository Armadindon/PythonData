from dataScripts import addToCommunes, getElectionData, getElectionDataByDept, simplifyGeoJson, xlsFilesToCSV
import sys
import time

if __name__ == "__main__":

    print("===Lancement du programme d'installation des dépendances===")
    full = "--full" in sys.argv or "-f" in sys.argv

    print("On ajoute les communes 'manquantes'")
    addToCommunes.main()

    if full: #En clonant le repository git, cette étape n'est pas nécéssaire
        print("ATTENTION : Cette partie risque de prendre beaucoup de temps ! (jusqu'a 12h)")
        print("Ne perdez pas la connexion, ou ne mettez pas fin à ce script durant cette période\n\n")

        print("On récupère les données de vote par ville\n")
        time.sleep(2) #On met un peu de temps afin que l'on puisse lire le programme
        getElectionData.main()

        print("On récupère les données de vote par départements\n")
        time.sleep(2) #On met un peu de temps afin que l'on puisse lire le programme
        getElectionDataByDept.main()
    
    print("On formate les geojson comme nécéssaire")
    simplifyGeoJson.main()

    print("On récupère les données du xls pour les mettres en csv")
    xlsFilesToCSV.main()

    print("===Fin du programme d'installation des dépendances===")

