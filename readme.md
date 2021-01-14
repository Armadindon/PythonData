# Python Data Vizualization

Projet réalisé pour l'ESIEE Paris, promotion 2020.

Toutes les commandes présentées dans ce document sont à lancer depuis la racine du projet.


## Installation

Clonez ce repository, si vous voulez récupérer les données, lancez cette ligne de commande :

```shell
python3 install.py
```

### Installation complète

Cette partie n'est pas nécéssaire, mais si souhaitée, il est possible de re-genérer les données de vote en faisant 

```shell
python3 install.py --full
```

**Attention :** Ce script récupère une grande quantité de données, il faut par conséquent avoir une connexion stable tout au long de l'éxécution de celui-ci, de plus, le temps d'éxécution peut être très lent (Jusqu'a 8h sur un VPS).


## Sources :
  * [Résultats de l'élection](https://www.interieur.gouv.fr/Elections/Les-resultats/Presidentielles/elecresult__presidentielle-2017/(path)/presidentielle-2017/index.html)
  * [Liste des départements Français](https://www.data.gouv.fr/fr/datasets/departements-de-france/)
  * [Liste des communes de France](https://www.data.gouv.fr/fr/datasets/communes-de-france-base-des-codes-postaux/)
  * [GeoJson de france](https://github.com/gregoiredavid/france-geojson)
  * [Revenus fiscaux par commune](https://www.data.gouv.fr/fr/datasets/l-impot-sur-le-revenu-par-collectivite-territoriale/)


