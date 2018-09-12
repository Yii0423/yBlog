# Generated by Django 2.0.8 on 2018-09-12 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yii', '0018_recall'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recall',
            old_name='imagesurl',
            new_name='bigurl',
        ),
        migrations.AddField(
            model_name='recall',
            name='smallurl',
            field=models.CharField(default='', max_length=500, verbose_name='图片缩略图'),
        ),
    ]