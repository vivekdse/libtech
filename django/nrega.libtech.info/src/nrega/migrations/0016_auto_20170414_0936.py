# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-14 04:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0015_auto_20170414_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panchayat',
            name='jobcardRegisterFile',
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
