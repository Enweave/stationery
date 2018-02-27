# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-27 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('orders', '0004_auto_20180223_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='auth.Group', verbose_name='группа')),
            ],
            options={
                'verbose_name_plural': 'настройки групп',
                'verbose_name': 'настройка групп',
                'default_related_name': 'group_settings',
            },
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['offer__title'], 'verbose_name': 'товар заказа', 'verbose_name_plural': 'товары заказа'},
        ),
    ]
