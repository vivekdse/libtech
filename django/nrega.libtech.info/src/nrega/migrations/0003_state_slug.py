# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 04:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0002_state_stateshortcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='slug',
            field=models.SlugField(default='a'),
            preserve_default=False,
        ),
    ]
