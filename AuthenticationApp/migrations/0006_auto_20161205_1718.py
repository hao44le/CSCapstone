# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0005_auto_20161201_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='programmingLanguage',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='speciality',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='yearsOfExperience',
            field=models.IntegerField(default=0, null=True),
        ),
    ]