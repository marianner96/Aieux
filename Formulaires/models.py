#!/usr/bin/python
# -*- coding:Utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django import forms

from django.forms import ModelForm

GENRES = (
    ('feminin', 'Féminin'),
    ('masculin', 'Masculin'),
)

## Définition des formulaires
class InscripConnecForm(forms.Form):
    inscrip_nom = forms.CharField(label='Nom ', required='required')
    inscrip_prenom = forms.CharField(label='Prenom ', required='required')
    inscrip_genre = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENRES, required='required')
    inscrip_ddn = forms.CharField(label='Date de naissance ', required='required')
    inscrip_email = forms.EmailField(label='E-mail', required='required')
    inscrip_mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')

    connec_email = forms.EmailField(label='E-mail', required='required')
    connec_mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')




class modifForm(forms.Form):
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

