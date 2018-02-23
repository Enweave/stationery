# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-23 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='company',
            field=models.CharField(blank=True, max_length=254, verbose_name='компания'),
        ),
        migrations.AddField(
            model_name='profile',
            name='inn',
            field=models.CharField(blank=True, max_length=254, verbose_name='ИНН'),
        ),
    ]
