# Projet GL1 : Mes Aieux
### Avant de démarrer
Se placer dans le dossier du projet, celui où il y a manage.py. 

Pour lancer le serveur : 
> python manage.py runserver

Si on obtien une erreur, cela est peut-être lié à la base de données. Pour mettre celle-ci à jour :
> python manage.py makemigration
> python manage.py migrate

Une fois le serveur démarré il devrait y avoir le message suivant : 
> Performing system checks...

> System check identified no issues (0 silenced).

> January 20, 2017 - 16:54:14

> Django version 1.10.2, using settings 'Aieux.settings'

> Starting development server at http://127.0.0.1:8000/

> Quit the server with CONTROL-C.

Il faut alors aller à l'adresse suivante : 
> http://127.0.0.1:0000/

A l'aide d'un navigateur quelconque.


Pour créer un super user : 

> python manage.py createsuperuser

Par défaut le super user que nous avons créé a les informations suivantes : 

Username : eisti

Email : eisti@eisti.eu

mdp : aieuxaieux

Ces identifiants nous permettent d'aller sur le module d'administration du site. Pour accéder à celui ci, une fois le serveur démarrer il faut rentrer l'url suivant : 

> http://127.0.0.1:0000/admin/

Puis ensuite on rentre l'identifiant eisti, et le mot de passe aieuxaieux.

### Auteurs : 
Ng Tock Mine Robin

Rentchler Marianne

Schall Anne-Gaëlle

Thibout Léa