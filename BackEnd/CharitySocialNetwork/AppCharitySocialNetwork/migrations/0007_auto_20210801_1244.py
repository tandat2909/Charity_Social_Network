# Generated by Django 3.2.5 on 2021-08-01 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCharitySocialNetwork', '0006_auto_20210731_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newspost',
            options={'ordering': ['-created_date']},
        ),
        migrations.AddField(
            model_name='newspost',
            name='is_show',
            field=models.BooleanField(default=False, help_text='Chỉ người duyệt bài mới cho phép thay đổi'),
        ),
    ]
