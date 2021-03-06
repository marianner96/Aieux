# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 13:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='autre_prenoms',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='famille',
            name='nb_personnes',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='adresse',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='famille',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Formulaires.Famille'),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='genre',
            field=models.CharField(blank=True, choices=[(b'feminin', b'feminin'), (b'masculin', b'masculin')], max_length=10),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='moderateur',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='nationalite',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='nom',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='prenom',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='profession',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='rang',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
