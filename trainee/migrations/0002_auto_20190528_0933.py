# Generated by Django 2.2.1 on 2019-05-28 09:33

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trainee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traineepage',
            name='intro',
            field=wagtail.core.fields.RichTextField(blank=True, max_length=128, verbose_name='简介'),
        ),
    ]