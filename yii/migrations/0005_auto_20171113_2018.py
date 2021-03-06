# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-13 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yii', '0004_essay'),
    ]

    operations = [
        migrations.AddField(
            model_name='essay',
            name='categoryid',
            field=models.IntegerField(default=0, verbose_name='所属分类编号'),
        ),
        migrations.AddField(
            model_name='essay',
            name='typeid',
            field=models.IntegerField(default=0, verbose_name='文章类型编号'),
        ),
        migrations.AlterField(
            model_name='essay',
            name='category',
            field=models.CharField(default=0, max_length=500, verbose_name='所属分类'),
        ),
        migrations.AlterField(
            model_name='essay',
            name='type',
            field=models.CharField(default=0, max_length=500, verbose_name='文章类型'),
        ),
    ]
