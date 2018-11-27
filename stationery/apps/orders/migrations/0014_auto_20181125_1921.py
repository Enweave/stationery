# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-25 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(blank=True, verbose_name='адрес доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.IntegerField(choices=[(1, 'Самовывоз'), (2, 'Почта России')], default=1, verbose_name='тип доставки'),
        ),
    ]