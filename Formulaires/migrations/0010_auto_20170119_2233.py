# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-19 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0009_auto_20170119_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fait_historique',
            name='arbre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Formulaires.Arbre'),
        ),
    ]
