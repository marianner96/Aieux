Pour lancer l'application Formulaires : 

Dans le terminal, une fois que l'on est dans le répertoire Aieux/ où il y a manage.py il faut tapper : 

python manage.py runserver

Puis ensuite on va dan sun navigateur et on va à l'adresse suivante : 

http://localhost:8000/Formulaires/



-----------------------------------------INFOS-------------------------------------------

Aieux/
    manage.py
    Aieux/
        __init__.py
        settings.py
        urls.py
        wsgi.py

    Formulaires/ 
    	... 
    	...


    Le premier répertoire racine Aieux/ n’est qu’un contenant pour le projet. Son nom n’a pas d’importance pour Django ; on peut le renommer comme vous voulez.

    manage.py : un utilitaire en ligne de commande qui permet d’interagir avec le projet Django de différentes façons. On y trouve toutes les informations nécessaires sur manage.py dans django-admin et manage.py.

    Le sous-répertoire Aieux/ correspond au paquet Python effectif de votre projet. C’est le nom du paquet Python que vous devrez utiliser pour importer ce qu’il contient (par ex. Aieux.urls).

    Aieux/__init__.py : un fichier vide qui indique à Python que ce répertoire doit être considéré comme un paquet.

    Aieux/settings.py : réglages et configuration du projet Django. Les réglages de Django vous apprendra tout sur le fonctionnement des réglages.

    Aieux/urls.py : les déclarations des URL de ce projet Django, une sorte de « table des matières » du site Django. 

    Aieux/wsgi.py : un point d’entrée pour les serveurs Web compatibles WSGI pour déployer le projet.
