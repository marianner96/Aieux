# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-20 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0020_merge_20170120_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='photo',
            field=models.ImageField(blank=True, upload_to=b'img/'),
        ),
    ]
