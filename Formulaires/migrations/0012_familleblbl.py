# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-19 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0011_fait_historique_type_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familleblbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=30)),
                ('nb_personnes', models.IntegerField(blank=True, default=1)),
            ],
        ),
    ]
