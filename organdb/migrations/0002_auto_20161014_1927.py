# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 17:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organdb.Region'),
        ),
    ]