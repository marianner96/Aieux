#!/usr/bin/python
# -*- coding:Utf-8 -*-

import hashlib
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
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
		FormConnection = UtilisateurForm(request.POST)
		if FormConnection.is_valid():
			mail = FormConnection.cleaned_data['email']
			mdp = FormConnection.cleaned_data['mdp']
			user = authenticate(username = mail, password = mdp)
			if user is not None: #Si pas dans la BDD : afficher un message d'erreur
				login(request, user)
				return redirect('Menu')
			else:
				return render(request,'accueilForm.html',{'FormConnection':FormConnection, 'error':error})
	else :
		FormConnection = UtilisateurForm()
		return render(request, 'accueilForm.html', {'FormConnection':FormConnection})


@login_required
def modificationForm(request):
	if request.method == 'POST':
		FormModif = UtilisateurForm(request.POST)
		if FormModif.is_valid():
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

			print(FormModif.errors)
			return render_to_response('Menu.html', {'FormModif':FormModif})
	else: 
		FormModif = UtilisateurForm()
	return render(request, 'modificationForm.html', {'FormModif':FormModif})


def Felicitations(request):
	return render(request, 'Felicitations.html')

def Menubis(request):
	return render(request, 'Menubis.html')

@login_required
def Menu(request):
	#Trouver un moyen pour récupérer la famille
	#essai = Utilisateur.objects.all()

	#essai = Utilisateur.objects.filter()
	#essai = request.user.email

	#Les groupes sont en fait les familles
	list_famille = Group.objects.all()

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
				group.permissions.add(Permission.objects.all())
        		group.save()
			form.save()

			user.groups.add(Group.objects.get(name = nom))			

			return redirect('Menu')
	else :
		ajoutFamille = FamilleForm()
	return render(request, 'Form_famille.html', {'ajoutFamille':ajoutFamille})

@login_required
def Rejoindre_famille(request):
	nom_session = (request.user).last_name
	famille = Famille.objects.filter(nom = nom_session)

	if request.method == 'POST':
		form = RejoindreForm(request.POST)
		if form.is_valid():
			val = form.cleaned_data['ajout']
			ajout_fam = Famille.objects.get(pk=val)
			ajout_fam.nb_personnes = ajout_fam.nb_personnes + 1
			ajout_fam.save()
			print(form.errors)

			#user.groups.add(Group.objects.get(name = val))

			return redirect('Menu')
	else :		
		form = RejoindreForm()
	return render(request, 'Rejoindre_famille.html', {'form':form ,'famille':famille})

@login_required
def Form_famille_ajoutmembre(request):
	return render(request, 'Form_famille_ajoutmembre.html')

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

