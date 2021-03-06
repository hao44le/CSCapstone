# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 21:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ProjectsApp', '0003_bookmarks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmarks',
            name='project',
        ),
        migrations.AddField(
            model_name='bookmarks',
            name='project',
            field=models.ManyToManyField(to='ProjectsApp.Project'),
        ),
        migrations.RemoveField(
            model_name='bookmarks',
            name='user',
        ),
        migrations.AddField(
            model_name='bookmarks',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
