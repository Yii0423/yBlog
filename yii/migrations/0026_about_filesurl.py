# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-13 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yii', '0025_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='filesurl',
            field=models.CharField(default='', max_length=100, verbose_name='文件链接'),
        ),
    ]