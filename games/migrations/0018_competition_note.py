# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-28 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0017_competition_competition_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
