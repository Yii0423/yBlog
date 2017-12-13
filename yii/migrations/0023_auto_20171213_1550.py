# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-13 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yii', '0022_auto_20171213_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='categoryid',
        ),
        migrations.AddField(
            model_name='about',
            name='type',
            field=models.CharField(default='', max_length=500, verbose_name='类型'),
        ),
        migrations.AddField(
            model_name='about',
            name='typeid',
            field=models.IntegerField(default=0, verbose_name='类型编号'),
        ),
    ]