# Generated by Django 2.2.1 on 2019-05-30 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainee', '0002_auto_20190528_0933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='traineeindexpage',
            options={'verbose_name': '学员列表页', 'verbose_name_plural': '学员列表页'},
        ),
        migrations.AlterModelOptions(
            name='traineepage',
            options={'verbose_name': '学员详情页', 'verbose_name_plural': '学员详情页'},
        ),
        migrations.AlterModelOptions(
            name='traineetagindexpage',
            options={'verbose_name': '学员动态页', 'verbose_name_plural': '学员动态页'},
        ),
    ]
