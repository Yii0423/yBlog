# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-13 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yii', '0021_auto_20171213_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='filesurl',
        ),
        migrations.AddField(
            model_name='about',
            name='categoryid',
            field=models.IntegerField(default=0, verbose_name='类型'),
        ),
        migrations.AddField(
            model_name='about',
            name='url',
            field=models.CharField(default='', max_length=100, verbose_name='链接'),
        ),
    ]