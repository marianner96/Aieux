# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0002_auto_20161219_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='famille',
            name='nom',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
