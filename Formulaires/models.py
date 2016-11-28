#!/usr/bin/python
# -*- coding:Utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone

import datetime

from django import forms
from django.utils import timezone
from django.forms import ModelForm

class Famille(models.Model):
    nom = models.CharField(max_length=30)
    nb_personnes = models.IntegerField(max_length=50)
    

GENRES = (
    ('feminin', 'Féminin'),
    ('masculin', 'Masculin'),
)

class ClassFormInscription(forms.Form):
    nom = forms.CharField(label='Nom ', required='required')
    prenom = forms.CharField(label='Prenom ', required='required')
    genre = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENRES, required='required')
    ddn = forms.CharField(label='Date de naissance ', required='required')
    email = forms.EmailField(label='E-mail', required='required')
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')

class ClassFormConnection(forms.Form):
    email = forms.EmailField(label='E-mail', required='required')
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')




class ClassmodifForm(forms.Form):
    #image = 
    nom = forms.CharField(label='Nom ', required='required', initial="nom bdd")
    prenom = forms.CharField(label='Prenom ', required='required', initial="prénom bdd")
    prenoms_autre = forms.CharField(label='Autres prénoms', initial="autres prénom bdd")
    genre = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENRES, required='required')
    ddn = forms.CharField(label='Date de naissance ', required='required', initial="date de naissance bdd")
    email = forms.EmailField(label='E-mail', required='required', initial="email bdd")
    postal = forms.CharField(label='Adresse postale', initial="adresse postale bdd")
    profession = forms.CharField(label='Profession', initial="profession bdd")
    description = forms.CharField(widget=forms.Textarea(), label='Description', initial="description bdd")
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')

"""class modifForm(forms.Form):
    #image = 
    modif_nom = forms.CharField(label='Nom ', required='required', initial="nom bdd")
    modif_prenom = forms.CharField(label='Prenom ', required='required', initial="prénom bdd")
    modif_prenoms_autre = forms.CharField(label='Autres prénoms', initial="autres prénom bdd")
    modif_genre = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENRES, required='required')
    modif_ddn = forms.CharField(label='Date de naissance ', required='required', initial="date de naissance bdd")
    modif_email = forms.EmailField(label='E-mail', required='required', initial="email bdd")
    modif_postal = forms.CharField(label='Adresse postale', initial="adresse postale bdd")
    modif_profession = forms.CharField(label='Profession', initial="profession bdd")
    modif_description = forms.CharField(widget=forms.Textarea(), label='Description', initial="description bdd")
    modif_mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')

"""