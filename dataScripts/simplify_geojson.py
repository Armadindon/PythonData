"""
Script permettant de récupérer l'architecture de dossier contenant les GeoJSON et
de la simplifier pour le lancement du script
"""
import sys
import os
import shutil

def main():
    """
    Fonction Principale
    """
    #on verifie que le dossier n'existe pas encore
    if "geojsonByDpt" in os.listdir("data"):
        sys.exit(0)

    #Sinon on fait une copie des données traitées
    os.mkdir(os.path.join("data","geojsonByDpt"))

    for dossier in os.listdir(os.path.join("data", "departements")):
        os.mkdir(os.path.join("data","geojsonByDpt", dossier.split("-")[0]))

        for file in os.listdir(os.path.join("data","departements",dossier)):
            if "communes" in file:
                shutil.copy(os.path.join("data","departements", dossier, file),
                os.path.join("data","geojsonByDpt",
                dossier.split("-")[0], "communes.geojson"))

if __name__ == "__main__":
    main()
