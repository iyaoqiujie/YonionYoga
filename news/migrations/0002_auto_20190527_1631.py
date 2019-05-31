# Generated by Django 2.2.1 on 2019-05-27 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='category',
            field=models.CharField(choices=[('news', '瑜伽动态'), ('wiki', '瑜伽百科')], default='infinite', max_length=16, verbose_name='新闻类别'),
        ),
    ]