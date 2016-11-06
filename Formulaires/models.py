#!/usr/bin/python
# -*- coding:Utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django import forms

GENRES = (
	('feminin', 'Féminin'),
	('masculin', 'Masculin'),
)

#class Image(models.Model):
#    image = models.ImageField(upload_to='Formulaires/images')

#Pour la BDD : 
#La table crée s'appellera Formulaires_utilisateur
class utilisateur(models.Model):
    #image
    nom = forms.CharField(label='Nom ', required='required')
    prenom = forms.CharField(label='Prenom ', required='required')
    prenoms_autre = forms.CharField(label='Autres prénoms')
    genre = forms.ChoiceField(widget=forms.RadioSelect, choices=GENRES, required='required')
    ddn = forms.CharField(label='Date de naissance ', required='required')
    email = forms.EmailField(label='E-mail', required='required')
    postal = forms.CharField(label='Adresse postale')
    profession = forms.CharField(label='Profession')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')


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

class modifForm(forms.Form):
#    image = Image.objects.get(name='profil_chat')
    nom = forms.CharField(label='Nom ', required='required')
    prenom = forms.CharField(label='Prenom ', required='required')
    prenoms_autre = forms.CharField(label='Autres prénoms')
    genre = forms.ChoiceField(widget=forms.RadioSelect, choices=GENRES, required='required')
    ddn = forms.CharField(label='Date de naissance ', required='required')
    email = forms.EmailField(label='E-mail', required='required')
    postal = forms.CharField(label='Adresse postale')
    profession = forms.CharField(label='Profession')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')

# Create your models here.