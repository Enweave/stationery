# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odinass', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='цена'),
        ),
    ]
