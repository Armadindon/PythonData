import os, shutil

#on verifie que le dossier n'existe pas encore
if "geojsonByDpt" in os.listdir("data"):
    exit(0)

#Sinon on fait une copie des données traitées
os.mkdir(os.path.join("data","geojsonByDpt"))

for dossier in os.listdir(os.path.join("data", "departements")):
    os.mkdir(os.path.join("data","geojsonByDpt", dossier.split("-")[0]))

    for f in os.listdir(os.path.join("data","departements",dossier)):
        if "communes" in f:
            shutil.copy(os.path.join("data","departements", dossier, f), os.path.join("data","geojsonByDpt", dossier.split("-")[0], "communes.geojson"))

