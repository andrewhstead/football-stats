# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-22 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_auto_20180821_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='bottom_primary_places',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='bottom_secondary_places',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='tie_breaker_1',
            field=models.CharField(choices=[('Goal Average', 'Goal Average'), ('Goal Difference', 'Goal Difference'), ('Goals Scored', 'Goals Scored'), ('Games Won', 'Games Won')], default='Goal Difference', max_length=25),
        ),
        migrations.AddField(
            model_name='competition',
            name='tie_breaker_2',
            field=models.CharField(choices=[('Goal Average', 'Goal Average'), ('Goal Difference', 'Goal Difference'), ('Goals Scored', 'Goals Scored'), ('Games Won', 'Games Won')], default='Goals Scored', max_length=25),
        ),
        migrations.AddField(
            model_name='competition',
            name='tie_breaker_3',
            field=models.CharField(blank=True, choices=[('Goal Average', 'Goal Average'), ('Goal Difference', 'Goal Difference'), ('Goals Scored', 'Goals Scored'), ('Games Won', 'Games Won')], max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='tie_breaker_4',
            field=models.CharField(blank=True, choices=[('Goal Average', 'Goal Average'), ('Goal Difference', 'Goal Difference'), ('Goals Scored', 'Goals Scored'), ('Games Won', 'Games Won')], max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='tie_breaker_5',
            field=models.CharField(blank=True, choices=[('Goal Average', 'Goal Average'), ('Goal Difference', 'Goal Difference'), ('Goals Scored', 'Goals Scored'), ('Games Won', 'Games Won')], max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='top_primary_places',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='top_secondary_places',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]