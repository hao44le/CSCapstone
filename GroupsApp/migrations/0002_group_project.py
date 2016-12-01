# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 02:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0001_initial'),
        ('GroupsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='project',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ProjectsApp.Project'),
        ),
    ]
