#!/usr/bin/python
# -*- coding:Utf-8 -*-

import hashlib

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from django.views import generic

from getpass import getpass

from .models import Utilisateur, Famille, Arbre, Fait_historique, UtilisateurForm

def InscriptionForm(request):
	if request.method == 'POST':
		#On s'occupe du formulaire d'inscription
		FormInscription = UtilisateurForm(request.POST)
		if FormInscription.is_valid():
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
			
			mdp = FormInscription.cleaned_data['mdp']
			email = FormInscription.cleaned_data['email']
			nom = FormInscription.cleaned_data['nom']

			FormInscription = UtilisateurForm(
				nom = FormInscription.cleaned_data['nom'],
				prenom = FormInscription.cleaned_data['prenom'],
				genre = FormInscription.cleaned_data['genre'],
				ddn = FormInscription.cleaned_data['ddn'],
				email = FormInscription.cleaned_data['email'],
				mdp = hashlib.sha1(mdp).hexdigest())

			FormInscription.save()

			user = User.objects.create_user(username = email, password = mdp)
			user.save()

			#Connexion automatique lors de l'inscription
			util = authenticate(username=email, password=mdp)
			login(request, util)

			#Vérifier si une famille existe lors de la création de l'utilisateur
			try:
				fam = Famille.objects.get(nom = nom)
			except ObjectDoesNotExist:
				redirect('/Form_famille/') #creation famille
			
			#Demande à l'utilisateur si il veut être dans une famille existante ou si il veut en créer une
			#form.moderateur = 0
			#On rajoute l'id de la famille à l'utilisateur
			#form.famille_id = fam.id
			#form.save()
			#rajouter autorisation de rentrer dans la famille
			
#			FormConnection.save()
			#authenticate(username = email, password = mdp)
		return render_to_response('Menu.html', {'FormInscription':FormInscription})

	else: 
		FormInscription = UtilisateurForm()
	return render(request, 'InscriptionForm.html', {'FormInscription':FormInscription})

def accueilForm(request):
	if request.method == 'POST':

		#On s'occupe du formulaire de connection
		FormConnection = UtilisateurForm(request.POST)
		if FormConnection.is_valid():
			mail = FormConnection.cleaned_data['email']
			mdp = FormConnection.cleaned_data['mdp']
			user = authenticate(username = mail, password = mdp)
			if user is not None:
				login(request, user)
				redirect('/Menu/') 
			else:
				mot = 'hello'
			
			return render_to_response('accueilForm.html', {'FormConnection':FormConnection})  
	else: 

		FormConnection = UtilisateurForm()
	return render(request, 'accueilForm.html', {'FormConnection':FormConnection})


@login_required
def modificationForm(request):
	if request.method == 'POST':
		FormModif = modifForm(request.POST)
		if FormModif.is_valid():
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est FormModif.save() et c'est tout mais bon ..
			#image = 
			nom = FormModif.cleaned_data['nom']
			prenom = FormModif.cleaned_data['prenom']
			prenoms_autre = FormModif.cleaned_data['prenoms_autre']
			genre = FormModif.cleaned_data['genre']
			ddn = FormModif.cleaned_data['ddn']
			email = FormModif.cleaned_data['email']
			postal = FormModif.cleaned_data['postal']
			profession = FormModif.cleaned_data['profession']
			description = FormModif.cleaned_data['description']
			mdp = FormModif.cleaned_data['mdp']

			FormModif.save()

			return render_to_response('modificationForm.html', {'FormModif':FormModif}, 
				context_instance=RequestContext(request))
	else: 
		FormModif = modifForm()
	return render(request, 'modificationForm.html', {'FormModif':FormModif})


def Felicitations(request):
	return render(request, 'Felicitations.html')

def Menubis(request):
	return render(request, 'Menubis.html')

@login_required
def Menu(request):
	return render(request, 'Menu.html')

@login_required
def Form_famille(request):
	if request.method == 'POST':
		ajoutFamille = Famille(request.POST)
		if ajoutFamille.is_valid():
			form = Famille(
				nom = ajoutFamille.cleaned_data['nom'],
				nb_personnes = 1)
			form.save()
	else :
		ajoutFamille = Famille()
	return render(request, 'Form_famille.html', {'ajoutFamille':ajoutFamille})

@login_required
def Form_famille_ajoutmembre(request):
	return render(request, 'Form_famille_ajoutmembre.html')

def Form_event(request):
	return render(request, 'Form_event.html')

def Confirm_ajoutevent(request):
	return render(request, 'Confirm_ajoutevent.html')