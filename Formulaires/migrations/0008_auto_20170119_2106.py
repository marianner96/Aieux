# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-19 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0007_utilisateur_validation_mdp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='ddn',
            field=models.CharField(blank=True, default=b'01-01-2000', max_length=10),
        ),
    ]
