# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yii', '0015_auto_20171118_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articleid', models.IntegerField(default=0, verbose_name='文章编号')),
                ('ip', models.CharField(default='', max_length=50, verbose_name='IP')),
                ('status', models.IntegerField(default=0, verbose_name='结果0-默认1-顶2-踩')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='city',
            field=models.CharField(default='', max_length=100, verbose_name='所在地'),
        ),
    ]
