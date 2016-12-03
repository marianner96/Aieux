#!/usr/bin/python
# -*- coding:Utf-8 -*-

import hashlib

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from django.views import generic

from getpass import getpass

#from .models import ClassFormInscription, ClassFormConnection, ClassmodifForm
from .models import Utilisateur, Famille, Arbre, Fait_historique



#def accueilForm(request):
#	return render(request, 'accueilForm.html')


############Tests inscription connection#############


##########################



def accueilForm(request):
	if request.method == 'POST':
		#On s'occupe du formulaire d'inscription
		FormInscription = Utilisateur(request.POST)
#		FormConnection = ClassFormConnection(request.POST)

		if FormInscription.is_valid():
			nom = FormInscription.cleaned_data['nom']
			prenom = FormInscription.cleaned_data['prenom']
			genre = FormInscription.cleaned_data['genre']
			ddn = FormInscription.cleaned_data['ddn']
			email = FormInscription.cleaned_data['email']
			mdp = FormInscription.cleaned_data['mdp']

			form = Utilisateur(nom, prenom, genre, ddn, email) 
			form.save()

			user = User.objects.create_user(username = email, password = mdp)
			user.save()

			#Vérifier si une famille existe lors de la création de l'utilisateur
			try:
				fam = Famille.objects.get(nom = nom)
			except ObjectDoesNotExist:
				print("Votre famille n'existe pas ! Voulez-vous la créer ?")
				#creation famille + changement de fonction
			
			#On change le statut de l'utilisateur
			#form.moderateur = 0
			#On rajoute l'id de la famille à l'utilisateur
			#form.famille_id = fam.id
			#form.save()
			# à faire avec les groupes ? + rajouter autorisation de rentrer dans la famille
			

#			FormConnection.save()
			#authenticate(username = email, password = mdp)
			return render_to_response('accueilForm.html', {'FormInscription':FormInscription},  
				contect_instance=RequestContext(request))
	else: 
		FormInscription = Utilisateur()
	return render(request, 'accueilForm.html', {'FormInscription':FormInscription},
		)

# pour décrypté un mot de passe, il faut crypté celui qu'on vient de recevoir avec celui deja dans la bdd
def FormConnection(request):
	if request.method == 'POST':
		#On s'occupe du formulaire d'inscription
		form = ClassFormConnection(request.POST)
		if form.is_valid():

			mail = form.cleaned_data['email']
			mdp = form.cleaned_data['mdp']

			user = authenticate(username = mail, password = mdp)
			if user is not None:
				mot = 'Coucou'
			else:
				mot = 'hello'

			return render_to_response('templates/accueilForm.html', {'FormConnection':form},  
				contect_instance=RequestContext(request))
	else: 
		form = ClassFormConnection()
	return render(request, 'accueilForm.html', {'FormConnection':form})



def modificationForm(request):
	if request.method == 'POST':
		form = modifForm(request.POST)
		if form.is_(valid):
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
			#image = 
			nom = form.cleaned_data['nom']
			prenom = form.cleaned_data['prenom']
			prenoms_autre = form.cleaned_data['prenoms_autre']
			genre = form.cleaned_data['genre']
			ddn = form.cleaned_data['ddn']
			email = form.cleaned_data['email']
			postal = form.cleaned_data['postal']
			profession = form.cleaned_data['profession']
			description = form.cleaned_data['description']
			mdp = form.cleaned_data['mdp']

			form.save()

			return render_to_response('modificationForm.html', {'form':form}, 
				contect_instance=RequestContext(request))
	else: 
		form = modifForm()
	return render(request, 'modificationForm.html', {'form':form})


def Felicitations(request):
	return render(request, 'Felicitations.html')

def Menubis(request):
	return render(request, 'Menubis.html')

def Menu(request):
	return render(request, 'Menu.html')

def Form_famille(request):
	return render(request, 'Form_famille.html')

def Form_famille_ajoutmembre(request):
	return render(request, 'Form_famille_ajoutmembre.html')

def Form_event(request):
	return render(request, 'Form_event.html')

def Confirm_ajoutevent(request):
	return render(request, 'Confirm_ajoutevent.html')