# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 14:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name_plural': 'Courses'},
        ),
        migrations.RenameField(
            model_name='course',
            old_name='mane',
            new_name='name',
        ),
    ]
