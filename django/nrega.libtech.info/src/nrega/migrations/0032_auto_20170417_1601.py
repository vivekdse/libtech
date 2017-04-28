# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import nrega.models


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0031_auto_20170417_0641'),
    ]

    operations = [
        migrations.CreateModel(
            name='nicBlockReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportFile', models.FileField(blank=True, null=True, upload_to=nrega.models.get_blockreport_upload_path)),
                ('reportType', models.CharField(max_length=16)),
                ('finyear', models.CharField(max_length=2)),
            ],
        ),
        migrations.AlterField(
            model_name='applicant',
            name='panchayat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nrega.Panchayat'),
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
            model_name='muster',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nrega.Block'),
        ),
        migrations.AlterField(
            model_name='panchayat',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nrega.Block'),
        ),
        migrations.AddField(
            model_name='nicblockreport',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nrega.Block'),
        ),
        migrations.AlterUniqueTogether(
            name='nicblockreport',
            unique_together=set([('block', 'reportType', 'finyear')]),
        ),
    ]
