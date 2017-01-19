#!/usr/bin/python
# -*- coding:Utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from django import forms
from django.forms import ModelForm


# id : identifiant unique de la famille (généré automatiquement)
# nom : nom de la famille
# nb_personnes : nombres de personnes présentes dans la famille
class Famille(models.Model):
    nom = models.CharField(max_length=30, blank=True)
    nb_personnes = models.IntegerField(default=1, blank=True)

    def __str__(self):
        return self.nom


class FamilleForm(ModelForm):
    class Meta:
        model = Famille
        fields = {'nom', 'nb_personnes'}
        labels = {'nom' : 'Nom', 'nb_personnes' : 'Nombre de personnes'}

# id : identifiant unique de l'utilisateur (généré automatiquement)
# nom : nom de l'utilisateur
# prenom : prénom de l'utilisateur
# genre : genre de l'utilisateur
# ddn : date de naissance de l'utilisateur
# email : e-mail de l'utilisateur
# mdp : mot de passe chiffré
# validation_mdp : validation du mot de passe mdp
# adresse : adresse de l'utilisateur
# profession : profession de l'utilisateur
# nationalite : nationalite de l'utilisateur
# description : description de l'utilisateur (optionnel)
# famille : identifiant de la famille si il y appartient
# rang : droit de l'utilisateur : 0 si c'est un utilisateur classique, 1 si c'est un historien et 2 si c'est un administrateur
# moderateur : savoir si l'utilisateur est modérateur de son groupe famille. Par défaut il l'est donc c'est égal à 1, sinon c'est égal à 0
class Utilisateur(models.Model):
    GENRES = (
        ('feminin', 'feminin'),
        ('masculin', 'masculin'),
    )
    nom = models.CharField(max_length=30, blank=True)
    prenom = models.CharField(max_length=30, blank=True)
    autre_prenoms = models.CharField(max_length=60, blank=True)
    genre = models.CharField(max_length=10, choices=GENRES, blank=True)
    ddn = models.CharField(max_length=10, blank=True, default="")
    email = models.EmailField()
    mdp = models.CharField(max_length=10)
    validation_mdp = models.CharField(max_length=10, default='')
    adresse = models.CharField(max_length=200, blank=True)
    profession = models.CharField(max_length=60, blank=True)
    nationalite = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=200, blank=True)
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE, null=True, blank=True)
    rang = models.IntegerField(default=0, blank=True)
    moderateur = models.IntegerField(default=1, blank=True)

    def __str__(self):
        return self.email

class UtilisateurForm(ModelForm):
    mdp = forms.CharField(widget=forms.PasswordInput)
    validation_mdp = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = Utilisateur
        fields = ['nom','prenom','autre_prenoms','genre','ddn','email','mdp','adresse','profession','nationalite','description','famille','rang','moderateur']
        labels = {
            'nom':'Nom',
            'prenom':'Prénom',
            'autres_prenoms':'Autres prénoms',
            'genre':'Genre',
            'ddn':'Date de naissance',
            'email':'E-mail',
            'mdp':'Mot de passe',
            'validation_mdp' : 'Confirmation mot de passe',
            'adresse':'Adresse postale',
            'profession':'Profession',
            'nationalite':'Nationalité',
            'description':'Description',
        }
        widgets = {'genre':forms.RadioSelect}

    def clean_validation_mdp(self):
        #Si le mdp est le même que le validation_mdp, alors on connecte l'utilisateur, si non on affiche un message d'erreur
        pass1 = self.cleaned_data.get('mdp')
        pass2 = self.cleaned_data.get('validation_mdp')

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Mots de passe différents")
        
        return self.cleaned_data

   
# id : identifiant unique de l'arbre de la famille généré automatiquement)
# famille : identifiant de la famille auquel appartient l'arbre  
class Arbre(models.Model):
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE)


# arbre : l'identifiant de l'arbre sur lequel ce fait est relié
# code : code du fait : 1 si naissance, 2 si mariage, 3 si décès, 4 si voyage, 5 si immigration, 6 si ville
# commentaire : commentaire que l'utilisateur peut mettre pour chaque évènement
#### naissance
# nom_enfant : le nom de l'enfant
# prenom_enfant : le prénom de l'enfant
# genre_enfant : le genre de l'enfant
# prenom_mere : le prénom de la mère de l'enfant
# prenom_pere : le prénom du père de l'enfant
# date_naissance : la date de naissance de l'enfant
#### mariage
# prenom_marie_1 : le prénom du premier marié
# prenom_marie_2 : le prénom du deuxième marié
# nom_famille : le nom de famille des mariés (on considère que l'un prend le nom de l'autre)
# date_mariage : la date du mariage
#### décès
# prenom_defunt : le prénom du défunt
# nom_defunt : le nom du défunt
# date_deces : la date de décès
#### voyage
# lieu_voyage : le lieu du voyage
# date_debut : la date du début du voyage
# date_fin : la date de fin du voyage
#### immigration
# pays_depart : le pays de départ de la personne
# pays_arrive : le pays d'arrivé
# date_immig : la date d'immigration
#### ville habitée
# ville : le nom de la ville
# date_arrive : la date d'arrivé dans la ville
# date_depart : la date de départ (si il y a lieu)
class Fait_historique(models.Model):
    GENRES = (
        ('feminin', 'feminin'),
        ('masculin', 'masculin'),
    )
    arbre = models.ForeignKey(Arbre, on_delete=models.CASCADE)
    code = models.IntegerField()
    commentaire = models.CharField(max_length=200, blank=True)
    #naissance
    nom_enfant = models.CharField(max_length=30, blank=True)
    prenom_enfant = models.CharField(max_length=30, blank=True)
    genre_enfant = models.CharField(max_length=10, choices=GENRES, blank=True)
    prenom_mere = models.CharField(max_length=30, blank=True)
    prenom_pere = models.CharField(max_length=30, blank=True)
    date_naissance = models.DateField(blank=True, null=True)
    #mariage
    prenom_marie_1 = models.CharField(max_length=30, blank=True)
    prenom_marie_2 = models.CharField(max_length=30, blank=True)
    nom_famille = models.CharField(max_length=30, blank=True)
    date_mariage = models.DateField(blank=True, null=True)
    #décès
    prenom_defunt = models.CharField(max_length=30, blank=True)
    nom_defunt = models.CharField(max_length=30, blank=True)
    date_deces = models.DateField(blank=True, null=True)
    #voyage
    lieu_voyage = models.CharField(max_length=30, blank=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    #immigration
    pays_depart = models.CharField(max_length=30, blank=True)
    pays_arrive = models.CharField(max_length=30, blank=True)
    date_immig = models.DateField(blank=True, null=True)
    #ville habitée
    ville = models.CharField(max_length=30, blank=True)
    date_arrive = models.DateField(blank=True, null=True)
    date_depart = models.DateField(blank=True, null=True)

class Fait_historiqueForm(ModelForm):
    class Meta:
        model = Fait_historique
        fields = ['arbre','code','commentaire',
        'nom_enfant','prenom_enfant','genre_enfant','prenom_mere','prenom_pere','date_naissance',
        'prenom_marie_1','prenom_marie_2','nom_famille','date_mariage',
        'prenom_defunt','nom_defunt','date_deces',
        'lieu_voyage','date_debut','date_fin',
        'pays_depart','pays_arrive','date_immig',
        'ville','date_arrive','date_depart']
        labels = {
            'commentaire':'Commentaire',
            'nom_enfant':'Nom de l\'enfant',
            'prenom_enfant':'Prénom de l\'enfant',
            'genre_enfant' : 'Genre de l\'enfant',
            'prenom_mere' : 'Prénom de la mère',
            'prenom_pere' : 'Prénom du père',
            'date_naissance' : 'Date de naisance',

            'prenom_marie_1' : 'Prénom de la/du premier(ère) marié(e)',
            'prenom_marie_2' : 'Prénom de la/du deuxième marié(e)',
            'nom_famille' : 'Nom de la famille', 
            'date_mariage' : 'Date du mariage',

            'prenom_defunt' : 'Prénom du défunt',
            'nom_defunt' : 'Nom du défunt',
            'date_deces' : 'Date du décès',

            'lieu_voyage' : 'Lieu du voyage',
            'date_debut' : 'Date de début du voyage', 
            'date_fin' : 'Date de fin du voyage', 

            'pays_depart' : 'Pays de départ',
            'pays_arrive' : 'Pays d\'arrivé',
            'date_immig' : 'Date de l\'immigration',

            'ville' : 'Ville habitée', 
            'date_arrive' : 'Date d\'arrivée',
            'date_depart' : 'Date de départ',
        }
        widgets = {'genre_enfant':forms.RadioSelect}