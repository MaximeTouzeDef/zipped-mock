Vous trouverez dans ce dossier un sous-dossier dans lequel il y a une api mockée grace à wiremock standalone. Pour la lancer, il suffit d'utiliser une des deux commandes décrites dans le fichier 'run'.


Cependant, actuellement l'API sera "vide".
Afin de la remplir, ouvrez un terminal dans le dossier à la racine (celui dans lequel est ce readme), puis utilisez la commande "python3 generator.py"
en cas de soucis, soit il faut simplement créer des dossiers vides, soit il y a un bug, dans ce cas, me contacter via l'adresse maxime.touze@intradef.gouv.fr


si vous travaillez en local, pensez à remettre le bon chemin vers le dossier PJ (à la main) dans le fichier body_example.json situé à la racine du projet, dans le champ "entries[0].path"


Afin de les tester, voici les liens vers mes workspaces postman :

https://lunar-trinity-924246.postman.co/workspace/SDemat~acfd2d54-836d-4bf3-813d-f965efc7bd3f/collection/27749011-09edbb88-19f8-45ae-8b59-78a8c625b752?action=share&creator=27749011

https://lunar-trinity-924246.postman.co/workspace/SDemat~acfd2d54-836d-4bf3-813d-f965efc7bd3f/collection/27749011-bbd8708b-f1ca-48b3-b6e7-21d4d743c006?action=share&creator=27749011

Après demande d'accès je devrai autoriser la lecture du postman.


Vous trouverez la liste des paramètres utilisables dans la véritable version dans le dossier "parametres"
Attention !
Dans la version actuelle de SDemat, le paramètre "obsolet" peut avoir les valeurs "oui" ou "non" (et non pas des booleens)

