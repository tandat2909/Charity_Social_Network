# Generated by Django 3.2.5 on 2021-09-18 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppCharitySocialNetwork', '0005_auto_20210918_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='info_auction', to='AppCharitySocialNetwork.newspost'),
        ),
    ]
