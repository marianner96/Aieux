#!/usr/bin/python
# -*- coding:Utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from bottle import Bottle, template, request, run
from django.http import HttpResponseRedirect

from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from django.views import generic

from .models import InscripConnecForm, modifForm

def accueilForm(request):
	return render(request, 'accueilForm.html')


############Tests inscription connection#############


##########################



def accueilForm(request):
	form = InscripConnecForm(request.POST)
	if request.method == 'POST':
		#On s'occupe du formulaire d'inscription

		if form.is_(valid):
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
			inscrip_nom = form.cleaned_data['inscrip_nom']
			inscrip_prenom = form.cleaned_data['inscrip_prenom']
			inscrip_genre = form.cleaned_data['inscrip_genre']
			inscrip_ddn = form.cleaned_data['inscrip_ddn']
			inscrip_email = form.cleaned_data['inscrip_email']
			inscrip_mdp = form.cleaned_data['inscrip_mdp']

			

		#On s'ocucpe du formulaire de connection
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
			connec_email = form.cleaned_data['connec_email']
			connec_mdp = form.cleaned_data['connec_mdp']


			form.save()

			return render_to_response('accueilForm.html', {'InscripConnecForm':InscripConnecForm},  
				contect_instance=RequestContext(request))
	else: 
		form = InscripConnecForm()
	return render(request, 'accueilForm.html', {'InscripConnecForm':InscripConnecForm})



def modificationForm(request):
	if request.method == 'POST':
		form = modifForm(request.POST)
		if form.is_(valid):
			#Il faut enregistrer tout ça dans la BDD ...
			#En fait je crois que c'est form.save() et c'est tout mais bon ..
			#image = 
			modif_nom = form.cleaned_data['modif_nom']
			modif_prenom = form.cleaned_data['modif_prenom']
			modif_prenoms_autre = form.cleaned_data['modif_prenoms_autre']
			modif_genre = form.cleaned_data['modif_genre']
			modif_ddn = form.cleaned_data['modif_ddn']
			modif_email = form.cleaned_data['modif_email']
			modif_postal = form.cleaned_data['modif_postal']
			modif_profession = form.cleaned_data['modif_profession']
			modif_description = form.cleaned_data['modif_description']
			modif_mdp = form.cleaned_data['modif_mdp']

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