# Generated by Django 3.2.5 on 2021-08-22 18:43

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCharitySocialNetwork', '0022_auto_20210816_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]