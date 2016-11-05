#!/usr/bin/python
# -*- coding:Utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django import forms

GENRES = (
	('feminin', 'Féminin'),
	('masculin', 'Masculin'),
)
	

class inscripForm(forms.Form):
    nom = forms.CharField(label='Nom ', required='required')
    prenom = forms.CharField(label='Prenom ', required='required')
    genre = forms.ChoiceField(widget=forms.RadioSelect, choices=GENRES, required='required')
    ddn = forms.CharField(label='Date de naissance ', required='required')
    email = forms.EmailField(label='E-mail', required='required')
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')

class connecForm(forms.Form):
    email = forms.EmailField(label='E-mail', required='required')
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')

# Create your models here.