# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odinass', '0007_auto_20171212_1527'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
