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
from .models import Utilisateur, Famille, Arbre, Fait_historique, UtilisateurForm


#def accueilForm(request):
#	return render(request, 'accueilForm.html')


def InscriptionForm(request):
	if request.method == 'POST':
		#On s'occupe du formulaire d'inscription
		FormInscription = UtilisateurForm(request.POST)

		#if FormInscription.is_valid():
		#	nom = FormInscription.cleaned_data['nom']

		if FormInscription.is_valid():
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
			
			mdp = FormInscription.cleaned_data['mdp']
			email = FormInscription.cleaned_data['email']

			form = Utilisateur(
				nom = FormInscription.cleaned_data['nom'], 
				prenom = FormInscription.cleaned_data['prenom'],
				genre = FormInscription.cleaned_data['genre'],
				ddn = FormInscription.cleaned_data['ddn'],
				email = FormInscription.cleaned_data['email'],
				mdp = hashlib.sha1(mdp).hexdigest())

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
		FormInscription = UtilisateurForm()
	return render(request, 'InscriptionForm.html', {'FormInscription':FormInscription},
		)

# pour décrypté un mot de passe, il faut crypté celui qu'on vient de recevoir avec celui deja dans la bdd
def accueilForm(request):
	if request.method == 'POST':
		#On s'occupe du formulaire d'inscription
		#form = ClassFormConnection(request.POST)
		#if form.is_valid():

		#On s'occupe du formulaire de connection
		FormConnection = UtilisateurForm(request.POST)
		if FormConnection.is_valid():
			mail = FormConnection.cleaned_data['email']
			mdp = FormConnection.cleaned_data['mdp']
			user = authenticate(username = mail, password = mdp)
			if user is not None:
				mot = 'Coucou'
			else:
				mot = 'hello'

			return render_to_response('templates/accueilForm.html', {'FormConnection':form},  
				contect_instance=RequestContext(request))
			#form.save()
			user = Utilisateur.objects.get(email=mail)
			
			#if (hashlib.sha1(mdp).hexdigest() == user.mdp):
				#on se connecte
			#else:
				#on envoie un message d'erreur
			
			return render_to_response('accueilForm.html', {'FormConnection':FormConnection},  
				context_instance=RequestContext(request))
	else: 
		FormConnection = UtilisateurForm()
	return render(request, 'accueilForm.html', {'FormConnection':FormConnection})



def modificationForm(request):
	if request.method == 'POST':
		FormModif = modifForm(request.POST)
		if FormModif.is_(valid):
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