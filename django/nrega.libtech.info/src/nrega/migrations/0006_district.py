# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 05:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0005_auto_20170410_0545'),
    ]

    operations = [
        migrations.CreateModel(
            name='district',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('fullDistrictCode', models.CharField(max_length=4, unique=True)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
    ]
