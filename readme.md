# Python Data Vizualization

Projet réalisé pour l'ESIEE Paris, promotion 2020.

Toutes les commandes présentées dans ce document sont à lancer depuis la racine du projet.



## Installation

Clonez ce repository, si vous voulez récupérer les données, lancer cette ligne de commande :

```shell
python3 dataScripts/getElectionData.py
```

**Attention :** Ce script récupère une grande quantité de données, il faut par conséquent avoir une connexion stable tout au long de l'éxécution de celui-ci, de plus, le temps d'éxécution peut être très lent.

Pour adapter les données des geoJson departements a notre programme, lancez le script simplifyGeoJson.py avec la commande:
```shell
python3 dataScripts/simplifyGeoJson.py
```

## Sources :
  -[Résultats de l'élection](https://www.interieur.gouv.fr/Elections/Les-resultats/Presidentielles/elecresult__presidentielle-2017/(path)/presidentielle-2017/index.html)
  -[Liste des départements Français](https://www.data.gouv.fr/fr/datasets/departements-de-france/)
  -[GeoJson de france](https://github.com/gregoiredavid/france-geojson)
  -[Revenus fiscaux par commune](#)


