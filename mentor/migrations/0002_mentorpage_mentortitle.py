# Generated by Django 2.2.1 on 2019-05-27 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorpage',
            name='mentortitle',
            field=models.CharField(blank=True, max_length=64, verbose_name='导师头衔'),
        ),
    ]