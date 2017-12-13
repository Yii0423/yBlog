# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-13 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yii', '0019_auto_20171213_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100, verbose_name='网站名')),
                ('logourl', models.CharField(default='', max_length=100, verbose_name='LOGO链接')),
                ('imagesurl', models.CharField(default='', max_length=500, verbose_name='BANNERS链接')),
                ('keywords', models.CharField(default='', max_length=1000, verbose_name='SEO关键词')),
                ('description', models.TextField(default='', verbose_name='SEO描述')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
        migrations.RemoveField(
            model_name='about',
            name='imagesurl',
        ),
        migrations.RemoveField(
            model_name='about',
            name='leading',
        ),
        migrations.RemoveField(
            model_name='about',
            name='logourl',
        ),
        migrations.AddField(
            model_name='about',
            name='filesurl',
            field=models.CharField(default='', max_length=100, verbose_name='文件链接'),
        ),
        migrations.AlterField(
            model_name='about',
            name='content',
            field=models.TextField(default='', verbose_name='描述'),
        ),
    ]