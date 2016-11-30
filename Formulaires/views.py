#!/usr/bin/python
# -*- coding:Utf-8 -*-

import hashlib

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
			#nom = FormInscription.cleaned_data['nom']
			#prenom = FormInscription.cleaned_data['prenom']
			#genre = FormInscription.cleaned_data['genre']
			#ddn = FormInscription.cleaned_data['ddn']
			#email = FormInscription.cleaned_data['email']
			#mdp = FormInscription.cleaned_data['mdp']

			form = Utilisateur(
				nom = FormInscription.cleaned_data['nom'], 
				prenom = FormInscription.cleaned_data['prenom'],
				genre = FormInscription.cleaned_data['genre'],
				ddn = FormInscription.cleaned_data['ddn'],
				email = FormInscription.cleaned_data['email'],
				mdp = hashlib.sha1(FormInscription.cleaned_data['mdp']).hexdigest()) 

			form.save()

			# il faudrait vérifier si une famille existe avec ce nom
			# si oui --> changer rang
			# si non --> la créer

			#ajouter id de la famille à familler_id du gars
			# form.famille_id = familledugars.id

			
#		if FormConnection.is_(valid):
		#On s'occupe du formulaire de connection
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
#			email = FormConnection.cleaned_data['email']
#			mdp = FormConnection.cleaned_data['mdp']

#			FormConnection.save()
			#il faudrait pouvoir se loguer quand on vient de s'inscrire 
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
		if form.is_(valid):

			mail = form.cleaned_data['email']
			mdp = form.cleaned_data['mdp']

			#form.save()
			user = Utilisateur.objects.get(email=mail)
			if (hashlib.sha1(mdp).hexdigest() == user.mdp) {
				#on se connecte
			} else {
				#on envoie un message d'erreur
			}

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