# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-14 03:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yii', '0008_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=500, verbose_name='留言')),
                ('replycontent', models.CharField(default='', max_length=500, verbose_name='回复')),
                ('ip', models.CharField(default='', max_length=50, verbose_name='IP')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remarks', models.TextField(default='', verbose_name='备注')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('isdel', models.BooleanField(default=False, verbose_name='是否删除')),
            ],
        ),
    ]
