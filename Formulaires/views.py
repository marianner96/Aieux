#!/usr/bin/python
# -*- coding:Utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from bottle import Bottle, template, request, run
from django.http import HttpResponseRedirect

from .models import inscripForm, connecForm, modifForm

def accueilForm(request):
	return render(request, 'Formulaires/accueilForm.html')

def inscriptionForm(request):
	if request.method == 'POST':
		form = inscripForm(request.POST)
		if form.is_(valid):
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
			nom = form.cleaned_data['nom']
			prenom = form.cleaned_data['prenom']
			genre = form.cleaned_data['genre']
			ddn = form.cleaned_data['ddn']
			email = form.cleaned_data['email']
			mdp = form.cleaned_data['mdp']

			form.save()

			return render_to_response('Formulaires/inscriptionForm.html', {'form':form}, 
				contect_instance=RequestContext(request))
	else: 
		form = inscripForm()
	return render(request, 'Formulaires/inscriptionForm.html', {'form':form})

def connectionForm(request):
	if request.method == 'POST':
		form = connecForm(request.POST)
		if form.is_(valid):
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
			email = form.cleaned_data['email']
			mdp = form.cleaned_data['mdp']

			form.save()

			return render_to_response('Formulaires/connectionForm.html', {'form':form}, 
				contect_instance=RequestContext(request))
	else: 
		form = connecForm()
	return render(request, 'Formulaires/connectionForm.html', {'form':form})

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

			return render_to_response('Formulaires/modificationForm.html', {'form':form}, 
				contect_instance=RequestContext(request))
	else: 
		form = modifForm()
	return render(request, 'Formulaires/modificationForm.html', {'form':form})


def Felicitations(request):
	return render(request, 'Formulaires/Felicitations.html')

### Ajout de template ...