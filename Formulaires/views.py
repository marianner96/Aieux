#!/usr/bin/python
# -*- coding:Utf-8 -*-

import hashlib
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.views import generic

from .models import Utilisateur, Famille, Arbre, Fait_historique, UtilisateurForm, FamilleForm, Fait_historiqueForm, RechercheForm
from .forms import RejoindreForm

from pprint import pprint
import os
from django.views.decorators.cache import never_cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}



# Fonction qui permet à l'utilisateur de s'inscrire
# La fonction redirige obligatoirement vers Rejoindre_Famille ou Form_famille car un utilisateur
# 		doit obligatoirement avoir une famille, même si il est le seul dans celle-ci.
def InscriptionForm(request):
	FormInscription = UtilisateurForm(request.POST or None, request.FILES)
	# Si la requête est POST on fait ce qui suit
	if request.method == 'POST':		
		# Vérifie si le formulaire est valide
		if FormInscription.is_valid():
			# On récupère les données dont on aura besoin pour le reste de la fonction
			mdp_session = FormInscription.cleaned_data['mdp']
			email_session = FormInscription.cleaned_data['email']
			nom_session = FormInscription.cleaned_data['nom']
			prenom_session = FormInscription.cleaned_data['prenom']
			photo_session = FormInscription.cleaned_data['photo']
			# On sauvegarde les données du formulaire dans la base de données
			FormInscription.save()

			# Créé une instance utilisateur à l'aide de l'email et le mot de passe
			user = User.objects.create_user(email_session, email=email_session, password=mdp_session)
			user.first_name = prenom_session
			user.last_name = nom_session
			# Sauvegarde l'utilisateur
			user.save()

			# Connexion automatique lors de l'inscription
			util = authenticate(username=email_session, password=mdp_session)
			login(request, util)

			# Vérifier si une famille existe lors de la création de l'utilisateur
			try:
				fam = Famille.objects.get(nom = nom_session)
			except ObjectDoesNotExist:
				return redirect('Form_famille') #creation famille
			except MultipleObjectsReturned:
				return redirect('Rejoindre_famille')
			
			# Demande à l'utilisateur si il veut être dans une famille existante ou si il veut en créer une			
			return redirect('Rejoindre_famille')

	return render(request, 'InscriptionForm.html', {'FormInscription':FormInscription})


# Connexion d'un utilisateur
def accueilForm(request):
	if request.method == 'POST':
		FormConnection = UtilisateurForm(request.POST)
		if FormConnection.is_valid():
			mail = FormConnection.cleaned_data['email']
			mdp = FormConnection.cleaned_data['mdp']
			user = authenticate(username = mail, password = mdp)
			# On vérifie si l'utilisateur est dans la base de données ou pas
			# Si ce n'est pas le cas, on affiche un message d'erreur
			if user is not None:
				login(request, user)
				return redirect('Menu')
			else:
				return render(request,'accueilForm.html',{'FormConnection':FormConnection})
		print(FormConnection.errors)
	else:
		FormConnection = UtilisateurForm()
	return render(request, 'accueilForm.html', {'FormConnection':FormConnection})


# Fonction qui permet à l'utilisateur, une fois connecté, de modifier ses informations
@login_required
def modificationForm(request):
	# On récupère l'utilisateur qui est connecté à l'aide de request.user
	user1 = User.objects.filter(email = request.user)
	user3 = Utilisateur.objects.filter(email = user1[0])
	user = user3[0]

	if request.method == 'POST':
		FormModif = UtilisateurForm(request.POST)
		print(FormModif.errors)
		if FormModif.is_valid():

			email = FormModif.cleaned_data['email']
			mdp = FormModif.cleaned_data['mdp']

			# On met à jour les champs dans la base de données
			obj = user3.update(
				nom = FormModif.cleaned_data['nom'],
				prenom = FormModif.cleaned_data['prenom'],
				photo = FormModif.cleaned_data['photo'],
				autre_prenoms = FormModif.cleaned_data['autre_prenoms'],
				genre = FormModif.cleaned_data['genre'],
				ddn = FormModif.cleaned_data['ddn'],
				email = FormModif.cleaned_data['email'],
				adresse = FormModif.cleaned_data['adresse'],
				profession = FormModif.cleaned_data['profession'],
				nationalite = FormModif.cleaned_data['nationalite'],
				description = FormModif.cleaned_data['description'],
				mdp = FormModif.cleaned_data['mdp']
			)

			# On reconnecte l'utilisateur, car le fait de modifier les champs le déconnecte
			user4 = authenticate(username = email, password = mdp)
			if user4 is not None:
				login(request, user4)
				return redirect('Menu')

			FormModif.save()

			return render_to_response('Menu.html', {'FormModif':FormModif,'user':user})
	else: 
		FormModif = UtilisateurForm()
		print(FormModif.errors)
	return render(request, 'modificationForm.html', {'FormModif':FormModif,'user':user})


# Fonction qui renvoie vers la page Menubis, le menu des visiteurs
def Menubis(request):
	if request.method == 'POST':
		recherche_form = RechercheForm(request.POST)
		if recherche_form.is_valid():
			search = recherche_form.cleaned_data['search']
			rech_pers = recherche_form.cleaned_data['rech_pers']
			rech_fam = recherche_form.cleaned_data['rech_fam']
			rech_page = recherche_form.cleaned_data['rech_page']

			res_pers = Utilisateur.objects.filter(prenom = search)
			res_fam = Famille.objects.filter(nom = search)
			
			#res_page : A faire quand on aura les images en fait
			res_page = ""

			return render(request, 'Menubis.html', {'res_pers':res_pers,'res_fam':res_fam,'res_page':res_page,'rech_pers':rech_pers,'rech_fam':rech_fam,'rech_page':rech_page})
		print(recherche_form.errors)
	else:
		recherche_form = RechercheForm()
		print(recherche_form.errors)

	return render(request, 'Menubis.html', {'recherche_form':recherche_form})


# Fonction qui permet de récupérer les familles et les faits historiques de l'utilisateur, ainsi que son nom et son prénom (request.user)
@login_required
def Menu(request):
	list_famille = request.user.groups.values_list('name',flat=True);
	longueur_list_famille = len(list_famille)

	fait_historique = Fait_historique.objects.filter(for_user = request.user)

	utilis = Utilisateur.objects.filter(email = request.user.email)[0]

	#Partie qui sert à la fonction de recherche
	if request.method == 'POST':
		recherche_form = RechercheForm(request.POST)
		if recherche_form.is_valid():
			search = recherche_form.cleaned_data['search']
			rech_pers = recherche_form.cleaned_data['rech_pers']
			rech_fam = recherche_form.cleaned_data['rech_fam']
			rech_page = recherche_form.cleaned_data['rech_page']

			res_pers = Utilisateur.objects.filter(prenom = search)
			res_fam = Famille.objects.filter(nom = search)
			
			#res_page : A faire quand on aura les images
			res_page = ""

			return render(request, 'res_recherche.html', {'res_pers':res_pers,'res_fam':res_fam,'res_page':res_page,'rech_pers':rech_pers,'rech_fam':rech_fam,'rech_page':rech_page})
		print(recherche_form.errors)
	else:
		recherche_form = RechercheForm()
		print(recherche_form.errors)

	return render(request, 'Menu.html', {'recherche_form':recherche_form,'list_famille':list_famille,'longueur_list_famille':longueur_list_famille,'utilis':utilis,'fait_historique':fait_historique})


# Fonction qui permet d'ajouter une nouvelle famille
@login_required
def Form_famille(request):
	if request.method == 'POST':
		ajoutFamille = FamilleForm(request.POST)
		if ajoutFamille.is_valid():
			nom = ajoutFamille.cleaned_data['nom']
			form = Famille(nom = nom)
			# On créé la nouvelle famille en tant que groupe
			group, created = Group.objects.get_or_create(name = nom)
			if created:
				group.save()

        	form.save()
        	user = request.user
        	# On ajoute l'utilisateur à la famille qu'il vient de créer
        	user.groups.add(Group.objects.get(name = nom))

        	return redirect('Menu')
	else :
		ajoutFamille = FamilleForm()
	return render(request, 'Form_famille.html', {'ajoutFamille':ajoutFamille})


# Fonction qui permet à l'utilisateur de rejoindre une famille déjà créé
@login_required
def Rejoindre_famille(request):
	# On récupère l'utilisateur qui est connecté ainsi que sa famille
	user_session = request.user
	nom_session = (user_session).last_name
	famille = Famille.objects.filter(nom = nom_session)

	if request.method == 'POST':
		form = RejoindreForm(request.POST)
		if form.is_valid():
			# On ajoute une personne de plus à la famille
			val = form.cleaned_data['ajout']
			ajout_fam = Famille.objects.get(pk = val)
			ajout_fam.nb_personnes = ajout_fam.nb_personnes + 1
			ajout_fam.save()

			# On ajoute la famille à l'utilisateur
			user_session.groups.add(Group.objects.get(name = ajout_fam))

			return redirect('Menu')
	else :		
		form = RejoindreForm()
	return render(request, 'Rejoindre_famille.html', {'form':form ,'famille':famille})

# Fonction qui permet d'ajouter un évènement. 
# code : 1 si naissance, 2 si mariage, 3 si décès, 4 si voyage, 5 si immigration, 6 si ville
# On enregistre à chaque fois le user associé pour pouvoir retrouver ensuite ses êvenements associés
def Form_event(request):
	if request.method == 'POST':
		ajoutevent = Fait_historiqueForm(request.POST)
		if ajoutevent.is_valid():
			code = ajoutevent.cleaned_data['code']
			if code == 1:
				ajoutevent = Fait_historique(type_event = "naissance", 
					for_user = request.user,
					commentaire = ajoutevent.cleaned_data['commentaire'],
					nom_enfant = ajoutevent.cleaned_data['nom_enfant'],
					prenom_enfant = ajoutevent.cleaned_data['prenom_enfant'],
					genre_enfant = ajoutevent.cleaned_data['genre_enfant'],
					prenom_mere = ajoutevent.cleaned_data['prenom_mere'],
					prenom_pere = ajoutevent.cleaned_data['prenom_pere'],
					date_naissance = ajoutevent.cleaned_data['date_naissance'],
				)
			elif code == 2:
				ajoutevent = Fait_historique(type_event = "mariage",
					for_user = request.user,
					commentaire = ajoutevent.cleaned_data['commentaire'],
					prenom_marie_1 = ajoutevent.cleaned_data['prenom_marie_1'],
					prenom_marie_2 = ajoutevent.cleaned_data['prenom_marie_2'],
					nom_famille = ajoutevent.cleaned_data['nom_famille'],
					date_mariage = ajoutevent.cleaned_data['date_mariage'],
				)
			elif code == 3:
				ajoutevent = Fait_historique(type_event = "deces",
					for_user = request.user,
					commentaire = ajoutevent.cleaned_data['commentaire'],
					prenom_defunt = ajoutevent.cleaned_data['prenom_defunt'],
					nom_defunt = ajoutevent.cleaned_data['nom_defunt'],
					date_deces = ajoutevent.cleaned_data['date_deces'],
				)
			elif code == 4:
				ajoutevent = Fait_historique(type_event = "voyage",
					for_user = request.user,
					commentaire = ajoutevent.cleaned_data['commentaire'],
					lieu_voyage = ajoutevent.cleaned_data['lieu_voyage'],
					date_debut = ajoutevent.cleaned_data['date_debut'],
					date_fin = ajoutevent.cleaned_data['date_fin'],
				)
			elif code == 5:
				ajoutevent = Fait_historique(type_event = "immigration",
					for_user = request.user,
					commentaire = ajoutevent.cleaned_data['commentaire'],
					pays_depart = ajoutevent.cleaned_data['pays_depart'],
					pays_arrive = ajoutevent.cleaned_data['pays_arrive'],
					date_immig = ajoutevent.cleaned_data['date_immig'],					
				)
			elif code == 6:
				ajoutevent = Fait_historique(type_event = "villehabitee",
					for_user = request.user,
					commentaire = ajoutevent.cleaned_data['commentaire'],
					ville = ajoutevent.cleaned_data['ville'],
					date_arrive = ajoutevent.cleaned_data['date_arrive'],
					date_depart = ajoutevent.cleaned_data['date_depart'],
				)

			ajoutevent.save()
			return redirect('Menu')
		print(ajoutevent.errors)
	else :
		ajoutevent = Fait_historiqueForm()
	return render(request, 'Form_event.html', {'ajoutevent':ajoutevent})

# Fonction de déconnexion
def logout_view(request):
	logout(request)
	return redirect('accueilForm')



#=====================================================================================================================
#==============================================FONCTION POUR L'ARBRE==================================================
#=====================================================================================================================
#Remplis les fichiers si sont vides

def initialise_fichier(request):
	error=None
	user1 = User.objects.filter(email = request.user)
	user2 = user1[0]
	user3 = Utilisateur.objects.filter(email = user2)
	nom = user3[0].nom
	prenom = user3[0].prenom

	if (user3[0].genre=="masculin"):
		sexe="m"
		img="/static/img/homme.jpeg"
	else:
		sexe="f"
		img="/static/img/femme.png"

	#si le fichier liste_couples est vide
	if (os.path.getsize("Formulaires/static/json/liste_couples.json")==0):
		contenu_c = '{ "couples" : }'
		fic = open ("Formulaires/static/json/liste_couples.json", "w")
		fic.write(contenu_c)
		fic.close()

	if (os.path.getsize("Formulaires/static/json/liste_enfants.json")==0):
		contenu_e = '{"orphelins": [{"nom": "'+nom+'", "prenom": "'+prenom+'", "sexe": "'+sexe+'", "parent": "non"}]}'
		fic = open ("Formulaires/static/json/liste_enfants.json", "w")
		fic.write(contenu_e)
		fic.close()

	if (os.path.getsize("Formulaires/static/json/liste_sans_conj.json")==0):
		contenu_sc = '{"sansconj":[{"nom": "'+nom+'", "prenom": "'+prenom+'", "sexe": "'+sexe+'"}]}'
		fic = open ("Formulaires/static/json/liste_sans_conj.json", "w")
		fic.write(contenu_sc)
		fic.close()

	if (os.path.getsize("Formulaires/static/json/nodesedges.json")==0):
		contenu = '{"nodes":[ {"id": 1, "shape": "image", "image": "'+img+'", "label":"'+nom+' '+prenom+'"}],"edges":[]}'
		fic = open ("Formulaires/static/json/nodesedges.json", "w")
		fic.write(contenu)
		fic.close()

	return render(request, template_name='arbre.html', context={"error":error})


@never_cache
def arbre(request):
    error = None
    return render(request, template_name='arbre.html', context={"error": error})

@never_cache
def add_membre_arbre(request):
    error = None
    return render(request, template_name='add_membre_arbre.html', context={"error": error})

@never_cache
def supp_membre_arbre(request):
    error = None
    return render(request, template_name='supp_membre_arbre.html', context={"error": error})

@never_cache
def maj_arbre(request):
    error = None
    return render(request, template_name='arbre.html', context={"error": error})

@never_cache#rempli le fichier modifs.json de la chaine passe en parametre = les modifs a mettre a jour dans l'arbre
def modifierfichier(request):
    print("---MODIFICATION DU FICHIER modifs.json-------------------------------------")

    t=request.GET['sontype']
    l=request.GET['sonlien']
    n=request.GET['sonnom']
    p=request.GET['sonprenom']
    s=request.GET['sonsexe']

    print("Mes variables: ")
    print(t)
    print(l)
    print(n)
    print(p)
    print(s)

    nouv_liste = '{ "nouv_membre" : [ {"type":"'+t+'"}, {"lienfamille":"'+l+'"}, {"nom":"'+n+'"}, {"prenom":"'+p+'"}, {"sexe":"'+s+'"} ]}'

    print("Fichier modifs (apres le remplissage): ")
    print(nouv_liste)

    fic = open ("Formulaires/static/json/modifs.json", "w")
    fic.write(nouv_liste)
    fic.close()

    return ""

@never_cache#utilisable via javascript : rajoute le nouveau membre a la liste des personnes sans conjoint grace a une requete
def maj_lsc(request):
    print("---MAJ LISTE SANS CONJOINT")
    mon_fichier = open("Formulaires/static/json/liste_sans_conj.json", "r")
    contenu = mon_fichier.read()
    mon_fichier.close()

    nouvelle_liste=contenu[:-2]+',{"nom":"'+request.GET['sonnom']+'","prenom":"'+request.GET['sonprenom']+'","sexe":"'+request.GET['sonsexe']+'"}]}'

    fic = open ("Formulaires/static/json/liste_sans_conj.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    return ""



@never_cache#Met a jour les listes correspondante a un nouveau parent
def maj_lnp(request):
    print("---MAJ LISTE NOUVEAU PARENT")
    #But 1: verifier si l'enfant du nouveau parent a deja un ou des parent(s) cad verifier s'il est dans la liste des enfants sans parents
    json_data=open('Formulaires/static/json/liste_enfants.json')
    data = json.load(json_data)
    #print("-------Contenu du fichier liste_enfants (SANS PARENTS): ")
    #print type(data) #dict
    #pprint(data)
    json_data.close()


    liste = data["orphelins"] #la liste des 'orphelins' de mon fichier liste_enfants
    enfant=request.GET['sonenfant'] #prenom et nom de l'enfant du nouveau parent

    nomCherche=enfant.split()[0] #juste le nom de l'enfant en question
    prenomCherche=enfant.split()[1] #juste le prenom de l'enfant en question

    i=0 #compteur permettant de trouver l'emplacement de l'enfant du nouveau parent  
    nomListe=liste[i]["nom"] #par defaut le premier nom enfant de la liste des orphelins
    prenomListe=liste[i]["prenom"] #idem pour le prenom

    #parcourt la liste des orphelins pour trouver l'enfant du nouveau parent
    while ((prenomCherche!=prenomListe) or (nomCherche!=nomListe)) and (i!=(len(liste)-1)): 
        i+=1
        nomListe=liste[i]["nom"]
        prenomListe=liste[i]["prenom"] 

    dictio = liste[i] #le dicionnaire correspondant a l'orphelin a etudier
    #print(dictio["parent"]) #le resultat de la cle parent = true ou false = s'il a deja un parent ou non

    nomp=request.GET['sonnom'] #du nouveau parent
    prenomp=request.GET['sonprenom']
    sexep=request.GET['sonsexe']

    if(dictio["parent"]!="non"): #si l'enfant a deja un (seul) parent 
        #Ajout d'un nouveau couple a la liste des couples
        #Puis enleve les deux amoureux de la liste des personnes sans conjoint
        #Et enleve l'enfant de la liste des enfants sans parents (enlever enfant du nouv parent)
        #Et aussi la liste des enfants sans parents (ajout du nouv parent)
        maj_np2(nomp,prenomp,dictio["parent"].split()[0],dictio["parent"].split()[1],nomCherche,prenomCherche,nomp,prenomp,sexep)

    else: #si l'enfant n'a aucun parent
        #met a jour la liste des personnes sans conjoint
        #met a jour la liste des enfants sans parents (modification du parametre parent a true)
        #Et aussi la liste des enfants sans parents (ajout du nouv parent)
        maj_np(i, data,(nomp+" "+prenomp),nomp,prenomp,sexep)
    
    return ""

@never_cache 
def maj_np(i, ancien_json,sonparent, sonnom, sonprenom, sonsexe):
    default=None
    #met a jour la liste des enfants sans parents 
    print("---MAJ LISTE ENFANT PARAMETRE")
    liste = ancien_json["orphelins"]
    nouvelle_liste = '{"orphelins":['
    j=0
    for enfant in range(len(liste)):
        re_enfant='{"nom": "'+liste[enfant]["nom"]+'", "prenom": "'+liste[enfant]["prenom"]+'", "sexe": "'+liste[enfant]["sexe"]
        if (enfant==i):
            nouv_dictio=re_enfant+'", "parent": "'+sonparent+'"},'
            nouvelle_liste=nouvelle_liste+nouv_dictio
        else: 
            remet_ordre=re_enfant+'", "parent": "'+liste[enfant]["parent"]+'"},' 
            nouvelle_liste=nouvelle_liste+remet_ordre

    nouvelle_liste=nouvelle_liste[:-1]+']}' #on enleve la derniere virgule et on ferme le crochet et l'accolade

    print("Fichier liste_enfants (apres ajout du parametre pour l'enfant du nouveau parent):")
    print(nouvelle_liste)

    mon_fichier = open("Formulaires/static/json/liste_enfants.json", "w")
    mon_fichier.write(nouvelle_liste)
    mon_fichier.close()


    #met a jour la liste des personnes sans conjoint
    #rajoute le nouveau membre a la liste des personnes sans conjoint

    print("---MAJ LISTE SANS CONJOINT BIS")
    mon_fichier2 = open("Formulaires/static/json/liste_sans_conj.json", "r")
    contenu2 = mon_fichier2.read()
    mon_fichier2.close()

    nouvelle_liste2=contenu2[:-2]+',{"nom":"'+sonnom+'","prenom":"'+sonprenom+'","sexe":"'+sonsexe+'"}]}'

    fic = open ("Formulaires/static/json/liste_sans_conj.json", "w")
    fic.write(nouvelle_liste2)
    fic.close()

    print("Fichier liste_sans_conj (apres ajout du nouveau membre):")
    print(nouvelle_liste2)


    #Ajoute un enfant dans la liste des enfants (sans parents)
    print("---MAJ LISTE ENFANTS (sans parents)")
    mon_fichier3 = open("Formulaires/static/json/liste_enfants.json", "r")
    contenu3 = mon_fichier3.read()
    mon_fichier3.close()

    nouvelle_liste=contenu3[:-2]+',{"nom":"'+sonnom+'","prenom":"'+sonprenom+'","sexe":"'+sonsexe+'", "parent": "non" }]}'

    fic = open ("Formulaires/static/json/liste_enfants.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_enfants (apres ajout du nouveau membre): ")
    print(nouvelle_liste)

    return default

def maj_np2(sonnom,sonprenom,sonnom2,sonprenom2, nomenfant, prenomenfant, nomp, prenomp, sexep):
    #Ajoute un nouveau couple dans la liste des couples
    print("---MAJ LISTE COUPLE")
    mon_fichier = open("Formulaires/static/json/liste_couples.json", "r")
    contenu = mon_fichier.read()
    mon_fichier.close()

    nouvelle_liste=contenu[:-2]+',{"nom":"'+sonnom+'","prenom":"'+sonprenom+'","nom2":"'+sonnom2+'", "prenom2": "'+sonprenom2+'" }]}'

    fic = open ("Formulaires/static/json/liste_couples.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_couples (apres ajout du couple)): ")
    print(nouvelle_liste)


    #Supprime deux personnes (le nouveau couple) de la liste des personnes sans conjoint
    print("---SUPPRIMER LISTE SANS CONJOINT")
    #Trouver et enlever le nouveau couple de la liste des personnes sans conjoint 
    json_data=open('Formulaires/static/json/liste_sans_conj.json')
    data = json.load(json_data)
    print("--------------Contenu du fichier liste_sans_conj: ")
    pprint(data)

    json_data.close()

    nouvelle_liste='{"sansconj":['

    liste = data["sansconj"] #la liste des personnes sans conj de mon fichier liste_sans_conj
    for personne in liste:
        #si le nom et le prenom de la personne ne correspond pas a ceux du couple 
        if ((personne["nom"]!=sonnom) or (personne["prenom"]!=sonprenom)) and ((personne["nom"]!=sonnom2) or (personne["prenom"]!=sonprenom2)):
            #il faut le/la garder dans la liste
            nouvelle_liste=nouvelle_liste+'{"nom": "'+personne["nom"]+'", "prenom": "'+personne["prenom"]+'", "sexe": "'+personne["sexe"]+'"},"'
        #et sinon on ne fait rien puisque le but est d'enlever le couple de la liste des personnes sans conjoint

    nouvelle_liste=nouvelle_liste[:-2]+']}'

    fic = open ("Formulaires/static/json/liste_sans_conj.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_sans_conj (apres la suppression du conj du couple)")
    print(nouvelle_liste)


    #Supprime un enfant de la liste des enfants (sans parents) le nom et prenom de l'enfant est passe en parametre (c'est l'enfant du nouveau couple)
    print("---SUPPRIMER LISTE ENFANT")
    #Trouver et enlever le nouveau couple de la liste des personnes sans conjoint 
    json_data=open('Formulaires/static/json/liste_enfants.json')
    data = json.load(json_data)
    print("--------------Contenu du fichier liste_enfants: ")
    pprint(data)
    json_data.close()

    nouvelle_liste='{"orphelins":['

    liste = data["orphelins"] #la liste des orphelins (=enfant avec un parent maximum)
    for enfant in liste:
        if ((enfant["nom"]!=nomenfant) or (enfant["prenom"]!=prenomenfant)):
            #il faut le/la garder dans la liste
            nouvelle_liste=nouvelle_liste+'{"nom": "'+enfant["nom"]+'", "prenom": "'+enfant["prenom"]+'", "sexe": "'+enfant["sexe"]+'", "parent": "'+enfant["parent"]+'"}, '

    nouvelle_liste=nouvelle_liste[:-2]+']}'

    fic = open ("Formulaires/static/json/liste_enfants.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_enfant (apres la suppression d'un enfant)")
    print(nouvelle_liste)


    #Rajoute le nouveau membre a la liste des enfants (sans parents)
    print("---MAJ LISTE ENFANTS (sans parents)")
    mon_fichier3 = open("Formulaires/static/json/liste_enfants.json", "r")
    contenu3 = mon_fichier3.read()
    mon_fichier3.close()

    nouvelle_liste=contenu3[:-2]+',{"nom":"'+nomp+'","prenom":"'+prenomp+'","sexe":"'+sexep+'", "parent": "non" }]}'

    fic = open ("Formulaires/static/json/liste_enfants.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_enfants (apres ajout du nouveau membre): ")
    print(nouvelle_liste)




@never_cache#Ajoute un enfant dans la liste des enfants (sans parents)
def add_enfant(sonnom,sonprenom,sonsexe):
    print("---MAJ LISTE ENFANTS (sans parents)")
    mon_fichier = open("Formulaires/static/json/liste_enfants.json", "r")
    contenu = mon_fichier.read()
    mon_fichier.close()

    nouvelle_liste=contenu[:-2]+',{"nom":"'+sonnom+'","prenom":"'+sonprenom+'","sexe":"'+sonsexe+'", "parent": "non" }]}'

    fic = open ("Formulaires/static/json/liste_enfants.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_enfants (apres ajout du nouveau membre): ")
    print(nouvelle_liste)

    return ""

@never_cache#Ajoute un nouveau couple dans la liste des couples
def add_couple(sonnom,sonprenom,sonnom2,sonprenom2):
    print("---MAJ LISTE COUPLE")
    mon_fichier = open("Formulaires/static/json/liste_couples.json", "r")
    contenu = mon_fichier.read()
    mon_fichier.close()

    nouvelle_liste=contenu[:-2]+',{"nom":"'+sonnom+'","prenom":"'+sonprenom+'","nom2":"'+sonnom2+'", "prenom2": "'+sonprenom2+'" }]}'

    fic = open ("Formulaires/static/json/liste_couples.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_couples (apres ajout du couple)): ")
    print(nouvelle_liste)

    return ""

@never_cache#Supprime deux personnes (le nouveau couple) de la liste des personnes sans conjoint
def supp_lsc(sonnom,sonprenom,sonnom2,sonprenom2):
    print("---SUPPRIMER LISTE SANS CONJOINT")
    #Trouver et enlever le nouveau couple de la liste des personnes sans conjoint 
    json_data=open('Formulaires/static/json/liste_sans_conj.json')
    data = json.load(json_data)
    print("--------------Contenu du fichier liste_sans_conj: ")
    pprint(data)

    json_data.close()

    nouvelle_liste='{"sansconj":['

    liste = data["sansconj"] #la liste des personnes sans conj de mon fichier liste_sans_conj
    for personne in liste:
        #si le nom et le prenom de la personne ne correspond pas a ceux du couple 
        if ((personne["nom"]!=sonnom) or (personne["prenom"]!=sonprenom)) and ((personne["nom"]!=sonnom2) or (personne["prenom"]!=sonprenom2)):
            #il faut le/la garder dans la liste
            nouvelle_liste=nouvelle_liste+'{"nom": "'+personne["nom"]+'", "prenom": "'+personne["prenom"]+'", "sexe": "'+personne["sexe"]+'"},"'
        #et sinon on ne fait rien puisque le but est d'enlever le couple de la liste des personnes sans conjoint

    nouvelle_liste=nouvelle_liste[:-2]+']}'

    fic = open ("Formulaires/static/json/liste_sans_conj.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_sans_conj (apres la suppression du conj du couple)")
    print(nouvelle_liste)

    return ""

@never_cache#Supprime un enfant de la liste des enfants (sans parents) le nom et prenom de l'enfant est passe en parametre
def supp_le(sonnom,sonprenom):
    print("---SUPPRIMER LISTE ENFANT")
    #Trouver et enlever le nouveau couple de la liste des personnes sans conjoint 
    json_data=open('Formulaires/static/json/liste_enfants.json')
    data = json.load(json_data)
    print("--------------Contenu du fichier liste_enfants: ")
    pprint(data)
    json_data.close()

    nouvelle_liste='{"orphelins":['

    liste = data["orphelins"] #la liste des orphelins (=enfant avec un parent maximum)
    for enfant in liste:
        if ((enfant["nom"]!=sonnom) or (enfant["prenom"]!=sonprenom)):
            #il faut le/la garder dans la liste
            nouvelle_liste=nouvelle_liste+'{"nom": "'+enfant["nom"]+'", "prenom": "'+enfant["prenom"]+'", "sexe": "'+enfant["sexe"]+'", "parent": "'+enfant["parent"]+'"}, '

    nouvelle_liste=nouvelle_liste[:-2]+']}'

    fic = open ("Formulaires/static/json/liste_enfants.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    print("Fichier liste_enfant (apres la suppression d'un enfant)")
    print(nouvelle_liste)

    return ""

@never_cache#Met a jour les listes concernes lorsque le nouveau membre est un conjoint
def maj_lnc(request):
    print("---MAJ LISTE NOUVEAU CONJOINT")
    #Ajout du nouveau couple a la liste 
    nom=request.GET['sonnom'] #nom du nouveau membre de la famille 
    prenom=request.GET['sonprenom'] #prenom du nouveau memebre de la famille

    conjoint=request.GET['sonconjoint'] 
    nomconj=conjoint.split()[0] #nom du conjoint du nouveau membre
    prenomconj=conjoint.split()[1] #prenom du conjoint du nouveau membre

    add_couple(nom,prenom,nomconj,prenomconj) #ajoute le nouveau couple a la liste

    #Ajout d'une nouvelle personne a la liste des enfants (sans parents)
    sexe=request.GET['sonsexe']
    add_enfant(nom,prenom,sexe)

    #Enleve son/ses enfants de la liste des enfants (sans parents)
    supp_les(nomconj,prenomconj)

    #Enleve son conjoint de la liste des personnes sans conjoint
    supp_lsc(nom,prenom,nomconj,prenomconj)
    return ""

@never_cache#Supprime les enfants de la listes des enfants (sans parents) du parent passe en parametre
def supp_les(nomconj,prenomconj):
    print("---SUPPRIMER LISTE ENFANTS")
    #Trouver et enlever le nouveau couple de la liste des personnes sans conjoint 
    json_data=open('Formulaires/static/json/liste_enfants.json')
    data = json.load(json_data)
    print("--------------Contenu du fichier liste_enfants: ")
    pprint(data)
    json_data.close()

    identiteParent=nomconj+" "+prenomconj;
    nouvelle_liste='{"orphelins":['

    liste = data["orphelins"] #la liste des orphelins (=enfant avec un parent maximum)
    for enfant in liste:
        if (enfant["parent"]!=identiteParent):
            #il faut le/la garder dans la liste
            nouvelle_liste=nouvelle_liste+'{"nom": "'+enfant["nom"]+'", "prenom": "'+enfant["prenom"]+'", "sexe": "'+enfant["sexe"]+'", "parent": "'+enfant["parent"]+'"}, '

    nouvelle_liste=nouvelle_liste[:-2]+']}'

    fic = open ("Formulaires/static/json/liste_enfants.json", "w")
    fic.write(nouvelle_liste)
    fic.close()

    return ""

@never_cache#met a jour le fichier nodesedges.json a partir du fichier modifs.json
def maj_nodes_edges(request):
    print("---MAJ DES NOEUDS")

    if (os.path.getsize("Formulaires/static/json/modifs.json")!=0): #si le fichier n'est pas vide = il a des modifs a faire

        json_data=open('Formulaires/static/json/nodesedges.json')
        data = json.load(json_data)
        #print("--------------Contenu du fichier nodesedges.json: ")
        #pprint(data)
        json_data.close()

        nodes=data["nodes"]
        edges=data["edges"]

        #print("La liste des nodes: ")
        #print(nodes)
        #print("La liste des edges: ")
        #print(edges)

        json_data2=open('Formulaires/static/json/modifs.json')
        data2 = json.load(json_data2)
        #print("--------------Contenu du fichier modifs.json: ")
        #pprint(data2)
        json_data2.close()

        membre=data2["nouv_membre"] #le nouveau membre a ajouter a l'arbre = liste
        print("le nouveau membre: ")
        print(membre)
        print(type(membre))

        if membre[0]["type"]=="enfant":
            #si le nouveau membre est un enfant
            maj_enfant(membre,nodes,edges)

        elif membre[0]["type"]=="parent":
            #si le nouveau membre est un parent
            maj_parent(membre,nodes,edges)
            #sonenfant=membre["lienfamille"]

        elif membre[0]["type"]=="couple":
            #si le nouveau membre est un conjoint
            maj_couple(membre,nodes,edges)
            #sonconjoint=membre["lienfamille"]

        else: #en theorie on ne devrait jamais avoir ce cas mais au cas ou...
            print("Erreur lors de la lecture du type du nouveau membre")

    else:
        print("Fichier vide, aucune modification n'est a faire!")


    return ""

@never_cache
def maj_enfant(membre,nodes,edges):
    print("---MAJ ENFANT")
    #Premier but: rajouter l'enfant a la liste des nodes
    sonparent=membre[1]["lienfamille"].split()[0]+" "+membre[1]["lienfamille"].split()[1]
    sonsexe=membre[4]["sexe"]

    nouv_nodes='"nodes":[ '

    for i in range(len(nodes)):
        j=i #indice a recuperer pour rajouter l'id du nouveau membre

        lab=nodes[i]["label"]

        if lab==sonparent:
            sonid=nodes[i]["id"] #id du parent a recuperer pour lier le nouveau membre et son parent

        if lab=="Mariage":
            nouv_nodes=nouv_nodes+'{"id": '+str(nodes[i]["id"])+', "label": "Mariage"},'
        else: 
            nouv_nodes=nouv_nodes+'{"id": '+str(nodes[i]["id"])+', "shape": "image", "image": "'+nodes[i]["image"]+'", "label":"'+lab+'"},'

    if sonsexe=="f": #choisi l'image en fonction du sexe du nouveau membre
        img="/static/img/femme.png"
    else:
        img="/static/img/homme.jpeg"

    idenfant=j+2
    nouv_nodes=nouv_nodes+'{"id": '+str(idenfant)+', "shape": "image", "image": "'+img+'", "label": "'+membre[2]["nom"]+' '+membre[3]["prenom"]+'"}], '

    #Deuxieme but: lier l'enfant au mariage de ses parents
    nouv_edges='"edges":[ '
    for k in range(len(edges)): #pour remettre le bon ordre et enlever les 'u'
        nouv_edges=nouv_edges+'{"from": '+str(edges[k]["from"])+', "to": '+str(edges[k]["to"])+'}, '
        if edges[k]["from"]==sonid: #si l'id du parent est dans la liste des edges 
            idmariage=edges[k]["to"] #on recupere l'id du mariage du parent pour y lier l'enfant

    nouv_edges=nouv_edges+'{"from": '+str(idmariage)+', "to": '+str(idenfant)+'} ] '

    nouv_nodes_edges='{ '+nouv_nodes+nouv_edges+' }'
    print("La nouvelle liste est: ")
    print(nouv_nodes_edges)

    #puis met a jour le fichier nodesedges.json
    fic = open ("Formulaires/static/json/nodesedges.json", "w")
    fic.write(nouv_nodes_edges)
    fic.close()

    #on vide le fichier modifs pour ne pas renvoyer les infos a chaque fois que l'utilisateur actualise la page
    fic = open ("Formulaires/static/json/modifs.json", "w")
    fic.write("")
    fic.close()
    
    return ""

@never_cache#met a jour le fichier nodesedges pour le cas d'un nouveau parent
def maj_parent(membre,nodes,edges):
    print("---MAJ PARENT")

    #Premier but: creer une nouvelle liste de nodes = rajouter les infos du nouveau membre dans la liste
    sonenfant=membre[1]["lienfamille"]
    sonsexe=membre[4]["sexe"]

    nouv_nodes='"nodes":[ '

    for i in range(len(nodes)):
        j=i #indice a recuperer pour rajouter l'id du nouveau membre

        lab=nodes[i]["label"]

        if lab==sonenfant:
            sonid=nodes[i]["id"] #id de l'enfant a recuperer pour lier le nouveau membre et son enfant

        if lab=="Mariage":
            nouv_nodes=nouv_nodes+'{"id": '+str(nodes[i]["id"])+', "label": "Mariage"},'
        else: 
            nouv_nodes=nouv_nodes+'{"id": '+str(nodes[i]["id"])+', "shape": "image", "image": "'+nodes[i]["image"]+'", "label":"'+lab+'"},'

    if sonsexe=="f": #choisi l'image en fonction du sexe du nouveau membre
        img="/static/img/femme.png"
    else:
        img="/static/img/homme.jpeg"

    idparent=j+2
    nouv_nodes=nouv_nodes+'{"id": '+str(idparent)+', "shape": "image", "image": "'+img+'", "label": "'+membre[2]["nom"]+' '+membre[3]["prenom"]+'"} '


    #Deuxieme but: creer une nouvelle liste de edges
    a_un_conjoint=False
    nouv_edges='], "edges":[ '
    for k in range(len(edges)): #pour remettre le bon ordre et enlever les 'u'
        nouv_edges=nouv_edges+'{"from": '+str(edges[k]["from"])+', "to": '+str(edges[k]["to"])+'}, '
        if edges[k]["to"]==sonid: #Cas ou il y a un edges qui arrive (to) a l'id de l'enfant = sonid
            # = cas ou le nouveau parent a un conjoint 
            idmariage=edges[k]["from"] #en fait dans ce cas c'est l'id du marriage
            a_un_conjoint=True

    if (not a_un_conjoint): #si la personne n'a pas de conjoint on rajoute un 'mariage'
        idmariage=(idparent+1)
        nouv_nodes=nouv_nodes+', {"id": '+str(idmariage)+', "label": "Mariage"}'

    nouv_edges=nouv_edges[:-1]+'{"from": '+str(idmariage)+', "to": '+str(sonid)+'}, {"from": '+str(idparent)+', "to": '+str(idmariage)+'} ] ' 

    nouv_nodes_edges='{ '+nouv_nodes+nouv_edges+' }'
    print("La nouvelle liste est: ")
    print(nouv_nodes_edges)

    #puis met a jour le fichier nodesedges.json
    fic = open ("Formulaires/static/json/nodesedges.json", "w")
    fic.write(nouv_nodes_edges)
    fic.close()

    #on vide le fichier modifs pour ne pas renvoyer les infos a chaque fois que l'utilisateur actualise la page
    fic = open ("Formulaires/static/json/modifs.json", "w")
    fic.write("")
    fic.close()
    
    return ""

@never_cache
def maj_couple(membre,nodes,edges):
    print("---MAJ COUPLE")
    #Premier but: mettre a jour la liste des nodes = cad rajouter une personne et potentiellement un mariage
    sonconj=membre[1]["lienfamille"]
    sonsexe=membre[4]["sexe"]
    #attention au cas ou le conjoint a deja des enfants (et un mariage)
    #et au cas ou la personne n'a pas encore d'enfant (donc mariage a creer)

    nouv_nodes='"nodes":[ '

    for i in range(len(nodes)):
        j=i #indice a recuperer pour rajouter l'id du nouveau membre

        lab=nodes[i]["label"]

        if lab==sonconj:
            sonid=nodes[i]["id"] #id du conjoint a recuperer pour lier le nouveau membre et son enfant

        if lab=="Mariage":
            nouv_nodes=nouv_nodes+'{"id": '+str(nodes[i]["id"])+', "label": "Mariage"},'
        else: 
            nouv_nodes=nouv_nodes+'{"id": '+str(nodes[i]["id"])+', "shape": "image", "image": "'+nodes[i]["image"]+'", "label":"'+lab+'"},'

    if sonsexe=="f": #choisi l'image en fonction du sexe du nouveau membre
        img="/static/img/femme.png"
    else:
        img="/static/img/homme.jpeg"

    idmembre=j+2
    nouv_nodes=nouv_nodes+'{"id": '+str(idmembre)+', "shape": "image", "image": "'+img+'", "label": "'+membre[2]["nom"]+' '+membre[3]["prenom"]+'"} '


    #Deuxieme but: creer une nouvelle liste de edges
    a_des_enfants=False
    nouv_edges='], "edges":[ '
    for k in range(len(edges)): #pour remettre le bon ordre et enlever les 'u'
        nouv_edges=nouv_edges+'{"from": '+str(edges[k]["from"])+', "to": '+str(edges[k]["to"])+'}, '
        if edges[k]["from"]==sonid: #Cas ou il y a un edges (from) qui a l'id du conjoint = sonid
            # = cas ou le conjoint a deja un mariage cad des enfants
            idmariage=edges[k]["to"] #en fait dans ce cas c'est l'id du marriage
            a_des_enfants=True

    if (not a_des_enfants): #si la personne n'a pas de conjoint 
        idmariage=(idmembre+1)
        nouv_nodes=nouv_nodes+', {"id": '+str(idmariage)+', "label": "Mariage"}' #on rajoute un 'mariage'
        nouv_edges=nouv_edges+'{"from": '+str(sonid)+', "to": '+str(idmariage)+'}, ' #on lie le conjoint au mariage

    nouv_edges=nouv_edges[:-1]+'{"from": '+str(idmembre)+', "to": '+str(idmariage)+'} ] ' #on lie le nouveau membre au mariage

    nouv_nodes_edges='{ '+nouv_nodes+nouv_edges+' }'
    print("La nouvelle liste est: ")
    print(nouv_nodes_edges)

    #puis met a jour le fichier nodesedges.json
    fic = open ("Formulaires/static/json/nodesedges.json", "w")
    fic.write(nouv_nodes_edges)
    fic.close()

    #on vide le fichier modifs pour ne pas renvoyer les infos a chaque fois que l'utilisateur actualise la page
    fic = open ("Formulaires/static/json/modifs.json", "w")
    fic.write("")
    fic.close()

    return ""


#Supprime le membre membre_a_supp de toutes les listes
def supprime_membre(request):
    membre_a_supp=request.GET['membre']
    #Supprime le membre de l'arbre = cad du fichier nodesedges
    print("---MAJ SUPP MEMBRE DE NODESEDGES: ")

    json_data=open('Formulaires/static/json/nodesedges.json') #lis le fichier nodes edges
    data = json.load(json_data)
    json_data.close()

    nodes=data["nodes"]
    edges=data["edges"]

    #Pour les nodes
    nouv_nodes='"nodes":[ '

    for i in range(len(nodes)):
        lab=nodes[i]["label"] #le label du ieme element de ma liste des nodes

        if lab=="Mariage": #si c'est un mariage
            nouv_nodes=nouv_nodes+'{"id": '+str(nodes[i]["id"])+', "label": "Mariage"},'

        elif (lab!=membre_a_supp): #si le label est different de la personne qu'on cherche
            nouv_nodes=nouv_nodes+'{"id": '+str(nodes[i]["id"])+', "shape": "image", "image": "'+nodes[i]["image"]+'", "label":"'+lab+'"},'

        else: #si c'est la personne que nous souhaitons supprimer, on recuper son id 
            sonid = i+1

    nouv_nodes=nouv_nodes[:-1]+' ], '

    #Pour les edges, les liens
    nouv_edges='"edges":[ '

    for k in range(len(edges)):
        if (edges[k]["from"]!=sonid) and (edges[k]["to"]!=sonid): #si le lien considere ne relie pas l'id de la personne supprime on le garde 
            nouv_edges=nouv_edges+'{"from": '+str(edges[k]["from"])+', "to": '+str(edges[k]["to"])+'},'
        #sinon on ne le recopie pas

    nouv_edges=nouv_edges[:-1]+' ] ' 

    nouv_nodes_edges='{ '+nouv_nodes+nouv_edges+' }'
    print("La nouvelle liste des nodes et edges est: ")
    print(nouv_nodes_edges)

    #puis met a jour le fichier nodesedges
    fic = open ("Formulaires/static/json/nodesedges.json", "w")
    fic.write(nouv_nodes_edges)
    fic.close()

    #Supprime le membre de la liste des couples (ainsi que son conjoint)
    print("---MAJ SUPP MEMBRE DE LISTE COUPLE: ")
    json_data=open('Formulaires/static/json/liste_couples.json') 
    data1 = json.load(json_data)
    json_data.close()

    liste_couples=data1["couples"]
    nouv_liste_couples='{ "couples" : ['
    conj="" #sert a enregistrer le conjoint du membre qu'on supprime au besoin

    for i in range(len(liste_couples)):
        nom1=liste_couples[i]["nom"]
        prenom1=liste_couples[i]["prenom"]
        identite1=nom1+' '+prenom1

        nom2=liste_couples[i]["nom2"]
        prenom2=liste_couples[i]["prenom2"]
        identite2=nom2+' '+prenom2

        if (identite1!=membre_a_supp) and (identite2!=membre_a_supp): #si aucune personne du couple etudie n'est la personne a supprimer on recopie le couple
            nouv_liste_couples=nouv_liste_couples+'{ "nom": "'+nom1+'", "prenom": "'+prenom1+'", "nom2": "'+nom2+'", "prenom2": "'+prenom2+'"},'
        else: #sinon il faut recuperer son conjoint (pour le mettre dans la liste des personnes sans conjoint)
            if (identite1!=membre_a_supp): #si la premiere personne n'est pas le membre a supprimer on garde son nom et son prenom
                nom_conjoint=nom1
                prenom_conjoint=prenom1 
                conj='{ "nom": "'+nom_conjoint+'", "prenom": "'+prenom_conjoint+'", "sexe": "m" },'
            else: #sinon cela signifie que c'est la deuxieme personne du couple
                nom_conjoint=nom2
                prenom_conjoint=prenom2
                conj='{ "nom": "'+nom_conjoint+'", "prenom": "'+prenom_conjoint+'", "sexe": "m" },'


    nouv_liste_couples=nouv_liste_couples[:-1]+' ]}'

    print("La nouvelle liste des couples est: ")
    print (nouv_liste_couples)

    #puis met a jour le fichier liste_couples
    fic1 = open ("Formulaires/static/json/liste_couples.json", "w")
    fic1.write(nouv_liste_couples)
    fic1.close()

    #Supprime le membre de la liste des enfants (sans parents) et l'enleve du parametre parent s'il y etait
    print("---MAJ SUPP MEMBRE DE LISTE ENFANTS: ")
    json_data=open('Formulaires/static/json/liste_enfants.json') 
    data2 = json.load(json_data)
    json_data.close()

    liste_orphelins=data2["orphelins"]
    nouv_liste_orphelins='{ "orphelins" : ['

    for j in range(len(liste_orphelins)):
        nom=liste_orphelins[j]["nom"]
        prenom=liste_orphelins[j]["prenom"]
        parent=liste_orphelins[j]["parent"]
        identite=nom+' '+prenom

        if (identite!=membre_a_supp): 
            if (parent==membre_a_supp): #si le (seul) parent de l'enfant est le membre a supprimer on lui enleve son parent
                parent="non"
            nouv_liste_orphelins=nouv_liste_orphelins+'{ "nom": "'+nom+'", "prenom": "'+prenom+'", "sexe": "'+liste_orphelins[j]["sexe"]+'", "parent": "'+parent+'"},'

    nouv_liste_orphelins=nouv_liste_orphelins[:-1]+' ]}'

    print("La nouvelle liste des orphelins est: ")
    print (nouv_liste_orphelins)

    #puis met a jour le fichier liste_enfants
    fic1 = open ("Formulaires/static/json/liste_enfants.json", "w")
    fic1.write(nouv_liste_orphelins)
    fic1.close()

    #Supprime le membre de la liste des personnes sans conjoint
    print("---MAJ SUPP MEMBRE DE LISTE SANS CONJOINT: ")
    json_data=open('Formulaires/static/json/liste_sans_conj.json') 
    data3 = json.load(json_data)
    json_data.close()

    liste_celib=data3["sansconj"]
    nouv_liste_celib='{ "sansconj" : [ '

    for j in range(len(liste_celib)):
        nom=liste_celib[j]["nom"]
        prenom=liste_celib[j]["prenom"]
        identite=nom+' '+prenom

        if (identite!=membre_a_supp): #si le membre etudie n'est pas le membre a supprimer on le laisse dans la liste des sans conjoints
            nouv_liste_orphelins=nouv_liste_orphelins+'{ "nom": "'+nom+'", "prenom": "'+prenom+'", "sexe": "'+liste_celib[j]["sexe"]+'"},'

    nouv_liste_celib=conj+nouv_liste_celib[:-1]+' ]}'

    print("La nouvelle liste des celibataire est: ")
    print (nouv_liste_celib)

    #puis met a jour le fichier liste_sans_conj
    fic1 = open ("Formulaires/static/json/liste_sans_conj.json", "w")
    fic1.write(nouv_liste_celib)
    fic1.close()


    return ""

#sending email
from django.core.mail import send_mail


def Envoi_Email(request):
	if request.method == 'POST':
		FormMail = UtilisateurForm(request.POST)
		if FormMail.is_valid():
			
			mdp_session = FormMail.cleaned_data['mdp']
			email_session = FormMail.cleaned_data['email']
			nom_session = FormMail.cleaned_data['nom']
			prenom_session = FormMail.cleaned_data['prenom']

			"""FormMail = UtilisateurForm(
				nom = FormMail.cleaned_data['nom'],
				prenom = FormMail.cleaned_data['prenom'],
				genre = FormMail.cleaned_data['genre'],
				ddn = FormMail.cleaned_data['ddn'],
				email = FormMailcleaned_data['email'],
				mdp = hashlib.sha1(mdp_session).hexdigest())"""

		return render(request,'Envoi_Email.html', {'FormMail':FormMail})

def renvoi_Email(request):
	return render(request, 'Envoi_Email.html')

def sendmail(request):
	message="Loren Ipsum"
	send_mail('Subject here',message,'eisti@eisti.eu',['ngtockmine@eisti.eu'],fail_silently=False,)
	return redirect('Menu')