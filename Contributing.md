# Python Data Vizualization

## Introduction
Ce document indique les différentes choses à vérifier avant de contribuer au projet, il indique aussi comment réaliser certaines actions.

## Comment contribuer
Tout d'abord, chaque nouvelle fonctionnalité / correction de bug se doit d'être effectuée sur une nouvelle branche, quand votre travail est terminé, faite une Pull/Merge Request.

### Les grands principes

1. Inspirez vous de ce qui à déja été fait
2. Ne réinventez pas la roue, si quelque chose à déjà été faite, reprenez le

### Les points à vérifier

1. Avant de commiter, vérifiez que le projet atteint un score minimum de **9.0/10 via pylint**, et de manière générale, visez toujours la note maximale sur les nouveaux fichiers que vous allez créer.
2. Avant de commiter, vérifiez que vous n'avez pas laissez certains éléments (Bloc de code commenté, Commentaire vide, etc.)
3. Avant de commiter, faites en sorte que votre message de commit aie un réel sens, si vous n'arrivez pas à trouver un message de commit, c'est peut être que votre commit est trop grosse et contient plusieurs ajouts / corrections
4. Avant de faire une Pull/Merge Request, n'oubliez pas de rebase votre branche actuelle sur master !

## Comment faire

### Comment ajouter un graphique
**Tout les graphiques "complexes" qui sont crée se doivent d'avoir un objet associé**

Si le type de graphique que vous souhaitez ajouter est déjà présent dans le dossier panels, ajoutez un nouvel objet dans le fichier, sur le modèle de ce qui a été déjà fait.
Dans l'autre cas, créez un fichier python dans le dossier panel et inspirez vous de ce qui à déjà été fait.

### Comment ajouter un onglet

1. Dans le fichier main.py, ajoutez dans la liste des liens HTML un nouvel élement de liste, avec la classe hide si il n'est pas affiché de base
2. Dans le fichier main.py, dans la fonction update_map, pensez à ajouter le fonctionnement inhérent à l'apparition de votre onglet sur le côté
3. Dans le fichier main.py, dans la fonction change_tab, Ajoutez un output et un input lié a votre nouvel onglet, gérez le cas ou l'on clique sur votre nouvel onglet (en renvoyant le contenu de votre onglet, ainsi que l'état des différents onglets).