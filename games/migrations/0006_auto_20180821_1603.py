# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 15:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_auto_20180821_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitions', to='games.League'),
        ),
    ]