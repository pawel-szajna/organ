# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organdb', '0018_sample_stop_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyboard',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='performer',
            name='died',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stop',
            name='length',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
