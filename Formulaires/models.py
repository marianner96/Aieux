#!/usr/bin/python
# -*- coding:Utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone


GENRES = (
    ('feminin', 'Feminin'),
    ('masculin', 'Masculin'),
)


class Famille(models.Model):
    nom = models.CharField(max_length=30)
    nb_personnes = models.IntegerField()


class Utilisateur(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    genre = models.CharField(max_length=8, choices=GENRES)
    ddn = models.DateField(blank=True, null=True)
    email = models.EmailField()
    mdp = models.CharField(widget=models.PasswordInput())
    adresse = models.CharField(max_length=200)
    profession = models.CharField(max_length=60)
    nationalite = models.CharField(max_length=200)
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE)
    rang = models.IntegerField(default=0)
    moderateur = models.IntegerField(default=1)
    
    
class Arbre(models.Model):
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE)

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
    prenom = forms.CharField(label='Prenom ', required='required', initial="prenom bdd")
    prenoms_autre = forms.CharField(label='Autres prenoms', initial="autres prenom bdd")
    genre = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENRES, required='required')
    ddn = forms.CharField(label='Date de naissance ', required='required', initial="date de naissance bdd")
    email = forms.EmailField(label='E-mail', required='required', initial="email bdd")
    postal = forms.CharField(label='Adresse postale', initial="adresse postale bdd")
    profession = forms.CharField(label='Profession', initial="profession bdd")
    description = forms.CharField(widget=forms.Textarea(), label='Description', initial="description bdd")
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')