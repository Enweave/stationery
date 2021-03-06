# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-11 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_kassa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('alfabank', 'Альфа-Клик'), ('apple_pay', 'Apple Pay'), ('b2b_sberbank', 'Сбербанк Бизнес Онлайн'), ('bank_card', 'Банковская карта'), ('cash', 'Наличные'), ('google_pay', 'Google Pay'), ('installments', 'Заплатить по частям'), ('mobile_balance', 'Баланс мобильного телефона'), ('psb', 'Интернет-банк Промсвязьбанка'), ('qiwi', 'QIWI Кошелек'), ('sberbank', 'Сбербанк Онлайн'), ('webmoney', 'Webmoney'), ('yandex_money', 'Яндекс.Деньги')], default='yandex_money', max_length=20, verbose_name='способ оплаты'),
        ),
    ]
