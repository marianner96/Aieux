# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-20 08:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0006_remove_utilisateur_validation_mdp'),
    ]

    operations = [
        migrations.AddField(
            model_name='fait_historique',
            name='for_user',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='fait_historique',
            name='type_event',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Formulaires.Fait_historique'),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='validation_mdp',
            field=models.CharField(default=b'', max_length=10),
        ),
        migrations.AlterField(
            model_name='fait_historique',
            name='arbre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Formulaires.Arbre'),
        ),
        migrations.AlterField(
            model_name='fait_historique',
            name='code',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='ddn',
            field=models.CharField(blank=True, default=b'', max_length=10),
        ),
    ]
