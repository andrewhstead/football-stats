# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-23 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0014_adjustment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='bottom_primary_places',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='competition',
            name='bottom_secondary_places',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='competition',
            name='top_primary_places',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='competition',
            name='top_secondary_places',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
