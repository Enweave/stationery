# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odinass', '0004_rest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(blank=True, choices=[(1, 'импорт'), (2, 'экспорт')], null=True, verbose_name='действие')),
                ('status', models.IntegerField(choices=[(1, 'импорт'), (2, 'экспорт'), (3, 'экспорт')], default=1, verbose_name='статус')),
                ('filename', models.CharField(max_length=254, verbose_name='название файла')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
    ]