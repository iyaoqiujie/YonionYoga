# Generated by Django 2.2.1 on 2019-05-30 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_coursepage_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseindexpage',
            options={'verbose_name': '课程列表页', 'verbose_name_plural': '课程列表页'},
        ),
        migrations.AlterModelOptions(
            name='coursepage',
            options={'verbose_name': '单门课程页', 'verbose_name_plural': '单门课程页'},
        ),
        migrations.AlterModelOptions(
            name='coursetagindexpage',
            options={'verbose_name': '热门课程页', 'verbose_name_plural': '热门课程页'},
        ),
    ]