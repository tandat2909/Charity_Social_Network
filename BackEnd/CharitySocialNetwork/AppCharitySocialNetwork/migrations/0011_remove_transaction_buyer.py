# Generated by Django 3.2.5 on 2021-10-07 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCharitySocialNetwork', '0010_alter_transaction_auction_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='buyer',
        ),
    ]
