# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organdb', '0016_auto_20161104_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyboard',
            name='instrument',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='organdb.Instrument'),
            preserve_default=False,
        ),
    ]