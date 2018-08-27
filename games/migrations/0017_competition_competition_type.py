# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-24 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0016_game_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='competition_type',
            field=models.CharField(choices=[('League', 'League'), ('Cup', 'Cup')], default='League', max_length=25),
        ),
    ]