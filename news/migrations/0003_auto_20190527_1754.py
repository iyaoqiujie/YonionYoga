# Generated by Django 2.2.1 on 2019-05-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20190527_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='intro',
            field=models.CharField(blank=True, max_length=256, verbose_name='简介'),
        ),
    ]
