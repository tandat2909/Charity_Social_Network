# Generated by Django 3.2.5 on 2021-10-06 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCharitySocialNetwork', '0007_auto_20211005_0049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='seller',
        ),
    ]
