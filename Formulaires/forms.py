import datetime

from django import forms
from django.utils import timezone
from django.forms import ModelForm
from models import Famille

GENRES = (
    ('feminin', 'Feminin'),
    ('masculin', 'Masculin'),
)

class Utilisateur(forms.Form):
    nom = forms.CharField(label='Nom', max_length=30)
    prenom = forms.CharField(label='Prenom', max_length=30)
    genre = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENRES, required='required')
    ddn = forms.DateTimeField('date published')
    email = forms.EmailField(label='E-mail', required='required')
    mdp = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe", required='required')
    adresse = forms.CharField(label='Adresse', max_length=200)
    profession = forms.CharField(label='Profession', max_length=60)
    nationalite = forms.CharField(label='Nationalite', max_length=30)
    description = forms.CharField(label='Description')
    rang = forms.IntegerField(label = 'rang')
    moderateur = forms.IntegerField(label='rang')