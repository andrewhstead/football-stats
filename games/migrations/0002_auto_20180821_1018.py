# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]