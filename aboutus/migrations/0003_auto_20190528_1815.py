# Generated by Django 2.2.1 on 2019-05-28 18:15

import aboutus.models
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0002_auto_20190528_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestonepage',
            name='body',
            field=wagtail.core.fields.StreamField([('milestone_list', wagtail.core.blocks.ListBlock(aboutus.models.EventBlock))]),
        ),
    ]
