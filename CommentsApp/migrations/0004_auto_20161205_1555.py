# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 15:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CommentsApp', '0003_comment_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='createdBy',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='group',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='GroupsApp.Group'),
        ),
    ]
