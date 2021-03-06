# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-13 23:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0013_auto_20170411_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='panchayat',
            name='jobcardRegisterFile',
            field=models.FileField(blank=True, null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='block',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nrega.District'),
        ),
        migrations.AlterField(
            model_name='district',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nrega.State'),
        ),
        migrations.AlterField(
            model_name='panchayat',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nrega.Block'),
        ),
    ]
