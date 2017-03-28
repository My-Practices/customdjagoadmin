# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 12:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20170328_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('state', models.BooleanField(default=False, verbose_name='Estado')),
                ('isDownload', models.BooleanField(default=False, verbose_name='¿Esta descargado?')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.CourseGroup')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cursos',
                'verbose_name': 'Curso',
            },
        ),
    ]