# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-18 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_office'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='телефон'),
        ),
    ]