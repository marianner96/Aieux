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

from .models import Utilisateur, Famille, Arbre, Fait_historique, UtilisateurForm, FamilleForm, Fait_historiqueForm
from .forms import RejoindreForm

def InscriptionForm(request):
	if request.method == 'POST':
		#On s'occupe du formulaire d'inscription
		FormInscription = UtilisateurForm(request.POST)
		if FormInscription.is_valid():
			
			mdp_session = FormInscription.cleaned_data['mdp']
			email_session = FormInscription.cleaned_data['email']
			nom_session = FormInscription.cleaned_data['nom']
			prenom_session = FormInscription.cleaned_data['prenom']
			FormInscription.save()

			user = User.objects.create_user(email_session, email=email_session, password=mdp_session)
			user.first_name = prenom_session
			user.last_name = nom_session
			user.save()

			#Connexion automatique lors de l'inscription
			util = authenticate(username=email_session, password=mdp_session)
			login(request, util)

			#Vérifier si une famille existe lors de la création de l'utilisateur
			try:
				fam = Famille.objects.get(nom = nom_session)
			except ObjectDoesNotExist:
				return redirect('Form_famille') #creation famille
			except MultipleObjectsReturned:
				return redirect('Rejoindre_famille')
			
			#Demande à l'utilisateur si il veut être dans une famille existante ou si il veut en créer une
			#rajouter autorisation de rentrer dans la famille
			
			return redirect('Rejoindre_famille')
	else: 
		FormInscription = UtilisateurForm()
	return render(request, 'InscriptionForm.html', {'FormInscription':FormInscription})

#Connexion d'un utilisateur
def accueilForm(request):
	if request.method == 'POST':
		print('post')
		FormConnection = UtilisateurForm(request.POST)
		if FormConnection.is_valid():
			print('valid')
			mail = FormConnection.cleaned_data['email']
			mdp = FormConnection.cleaned_data['mdp']
			user = authenticate(username = mail, password = mdp)
			if user is not None: #Si pas dans la BDD : afficher un message d'erreur
				login(request, user)
				return redirect('Menu')
			else:
				return render(request,'accueilForm.html',{'FormConnection':FormConnection})
		print(FormConnection.errors)
	else:
		FormConnection = UtilisateurForm()
	return render(request, 'accueilForm.html', {'FormConnection':FormConnection})



#Voir comment on peut enregistrer les informations de modification !
#S'arranger pour mettre la date comme il faut ...
#Encore modifier des trucs blblbl
@login_required
def modificationForm(request):
	user1 = User.objects.filter(email = request.user)
	user2 = user1[0]
	user3 = Utilisateur.objects.filter(email = user2)
	user = user3[0]

	if request.method == 'POST':
		FormModif = UtilisateurForm(request.POST)
		print(FormModif.errors)
		if FormModif.is_valid():

			email = FormModif.cleaned_data['email']
			mdp = FormModif.cleaned_data['mdp']

			obj, created = user3.update(
				nom = FormModif.cleaned_data['nom'],
				prenom = FormModif.cleaned_data['prenom'],
				autre_prenoms = FormModif.cleaned_data['autre_prenoms'],
				genre = FormModif.cleaned_data['genre'],
				ddn = FormModif.cleaned_data['ddn'],
				email = FormModif.cleaned_data['email'],
				adresse = FormModif.cleaned_data['adresse'],
				profession = FormModif.cleaned_data['profession'],
				nationalite = FormModif.cleaned_data['nationalite'],
				description = FormModif.cleaned_data['description'],
				mdp = FormModif.cleaned_data['mdp'],
			)

			user4 = authenticate(username = email, password = mdp)
			if user4 is not None: #Si pas dans la BDD : afficher un message d'erreur
				login(request, user4)
				return redirect('Menu')

			"""new_values = {'nom': FormModif.cleaned_data['nom'],
				'prenom': FormModif.cleaned_data['prenom'],
				'autre_prenoms' : FormModif.cleaned_data['autre_prenoms'],
				'genre' : FormModif.cleaned_data['genre'],
				'ddn' : FormModif.cleaned_data['ddn'],
				'email' : FormModif.cleaned_data['email'],
				'adresse' : FormModif.cleaned_data['adresse'],
				'profession' : FormModif.cleaned_data['profession'],
				'nationalite' : FormModif.cleaned_data['nationalite'],
				'description' : FormModif.cleaned_data['description'],
				'mdp' : FormModif.cleaned_data['mdp']
			}
			new_values.update()
			obj = user3(**new_values)
			obj.save()"""


			#user3.autre_prenoms.update(FormModif.cleaned_data['autre_prenoms'])
			
			"""nom = FormModif.cleaned_data['nom']
			prenom = FormModif.cleaned_data['prenom']
			prenoms_autre = FormModif.cleaned_data['prenoms_autre']
			genre = FormModif.cleaned_data['genre']
			ddn = FormModif.cleaned_data['ddn']
			email = FormModif.cleaned_data['email']
			postal = FormModif.cleaned_data['postal']
			profession = FormModif.cleaned_data['profession']
			description = FormModif.cleaned_data['description']
			mdp = FormModif.cleaned_data['mdp']"""

			FormModif.save()

			return render_to_response('Menu.html', {'FormModif':FormModif,'user':user})
	else: 
		FormModif = UtilisateurForm()
	return render(request, 'modificationForm.html', {'FormModif':FormModif,'user':user})


def Felicitations(request):
	return render(request, 'Felicitations.html')

def Menubis(request):
	return render(request, 'Menubis.html')

@login_required
def Menu(request):
	#Trouver un moyen pour récupérer la famille

	list_famille = request.user.groups.values_list('name',flat=True);

	#essai = Utilisateur.objects.filter()
	#essai = request.user.email

	#Les groupes sont en fait les familles
	#list_famille = Group.objects.all()

	#list_famille = Famille.objects.filter()
	longueur_list_famille = len(list_famille)
	return render(request, 'Menu.html', {'list_famille':list_famille,'longueur_list_famille':longueur_list_famille,'first_name':request.user.first_name,'last_name':request.user.last_name})

@login_required
def Form_famille(request):
	if request.method == 'POST':
		ajoutFamille = FamilleForm(request.POST)
		if ajoutFamille.is_valid():
			nom = ajoutFamille.cleaned_data['nom']
			form = Famille(nom = nom)
			group, created = Group.objects.get_or_create(name = nom)
			if created:
				#Pour l'instant on lui met toutes les permissions
				#group.permissions.add(Permission.objects.all())
				group.save()

        	form.save()
        	user = request.user
        	user.groups.add(Group.objects.get(name = nom))

        	return redirect('Menu')
	else :
		ajoutFamille = FamilleForm()
	return render(request, 'Form_famille.html', {'ajoutFamille':ajoutFamille})


@login_required
def Rejoindre_famille(request):
	user_session = request.user
	nom_session = (user_session).last_name
	famille = Famille.objects.filter(nom = nom_session)

	if request.method == 'POST':
		form = RejoindreForm(request.POST)
		if form.is_valid():
			val = form.cleaned_data['ajout']
			ajout_fam = Famille.objects.get(pk = val)
			ajout_fam.nb_personnes = ajout_fam.nb_personnes + 1
			ajout_fam.save()

			user_session.groups.add(Group.objects.get(name = ajout_fam))

			return redirect('Menu')
	else :		
		form = RejoindreForm()
	return render(request, 'Rejoindre_famille.html', {'form':form ,'famille':famille})

@login_required
def Form_famille_ajoutmembre(request):
	if request.method == 'POST':
		ajoutMembreForm = UtilisateurForm(request.POST)
		if ajoutMembreForm.is_valid():
			form.save()
			print(ajoutMembreForm.errors)
			return redirect('Menu')
	else :
		ajoutMembreForm = UtilisateurForm()
	return render(request, 'Form_famille_ajoutmembre.html', {'ajoutMembreForm':ajoutMembreForm})

def Form_event(request):
	if request.method == 'POST':
		ajoutevent = Fait_historiqueForm(request.POST)
		if ajoutevent.is_valid():
			"""code = FormModif.cleaned_data['code']
			if (code == '1'): 
				#naissance
			elif (code == '2'):
				#mariage
			elif (code == '3'):
				#décès
			elif (code == '4'):
				#voyage
			elif (code == '5'):
				#immigration
			elif (code == '6'):
				#ville"""

			form.save()
			print(ajoutevent.errors)
			return redirect('Menu')
	else :
		ajoutevent = Fait_historiqueForm()
	return render(request, 'Form_event.html', {'ajoutevent':ajoutevent})

def Confirm_ajoutevent(request):
	return render(request, 'Confirm_ajoutevent.html')


#fonction de déconnexion
def logout_view(request):
	logout(request)
	return redirect('accueilForm')

