# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-19 22:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0008_auto_20170119_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Formulaires.Fait_historique'),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='ddn',
            field=models.CharField(blank=True, default=b'', max_length=10),
        ),
    ]
