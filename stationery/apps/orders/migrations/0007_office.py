# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-18 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import orders.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_groupsettings_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254, verbose_name='название')),
                ('address', models.TextField(verbose_name='адрес')),
                ('phone', models.CharField(blank=True, max_length=254, verbose_name='телефон')),
                ('coordinates', orders.fields.YandexPointField(blank=True, null=True, srid=4326, verbose_name='координаты')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='порядок')),
            ],
            options={
                'verbose_name': 'офис',
                'verbose_name_plural': 'офисы',
                'ordering': ['order'],
            },
        ),
    ]