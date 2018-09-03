# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-03 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0020_auto_20180831_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='subsidiaries',
            field=models.ManyToManyField(blank=True, null=True, related_name='_competition_subsidiaries_+', to='games.Competition'),
        ),
    ]