# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-20 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaires', '0023_banqueimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banqueimages',
            name='photo1',
            field=models.ImageField(blank=True, default=b'', storage=b'img/test.jpg', upload_to=b''),
        ),
    ]