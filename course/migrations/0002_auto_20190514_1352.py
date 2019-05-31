# Generated by Django 2.2.1 on 2019-05-14 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepage',
            name='advantage',
            field=models.CharField(blank=True, max_length=256, verbose_name='课程优势'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='plan',
            field=models.CharField(default='每月-开课', max_length=64, verbose_name='课程安排'),
        ),
        migrations.AlterField(
            model_name='coursepage',
            name='intro',
            field=models.CharField(max_length=256, verbose_name='简介'),
        ),
    ]
