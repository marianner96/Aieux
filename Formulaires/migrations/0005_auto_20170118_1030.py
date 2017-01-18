# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-18 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0004_auto_20161219_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fait_historique',
            name='autre_nom',
        ),
        migrations.RemoveField(
            model_name='fait_historique',
            name='autre_prenom',
        ),
        migrations.RemoveField(
            model_name='fait_historique',
            name='date_fait',
        ),
        migrations.RemoveField(
            model_name='fait_historique',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='fait_historique',
            name='prenom',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='rang',
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='commentaire',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='date_arrive',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='date_debut',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='date_deces',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='date_depart',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='date_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='date_immig',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='date_mariage',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='date_naissance',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='genre_enfant',
            field=models.CharField(blank=True, choices=[(b'feminin', b'feminin'), (b'masculin', b'masculin')], max_length=10),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='lieu_voyage',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='nom_defunt',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='nom_enfant',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='nom_famille',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='pays_arrive',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='pays_depart',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='prenom_defunt',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='prenom_enfant',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='prenom_marie_1',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='prenom_marie_2',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='prenom_mere',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='prenom_pere',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='ville',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
