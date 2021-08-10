# Generated by Django 3.2.5 on 2021-07-30 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppCharitySocialNetwork', '0002_auto_20210728_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmotionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OptionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='newscategory',
            options={},
        ),
        migrations.AlterModelOptions(
            name='newspost',
            options={},
        ),
        migrations.RenameField(
            model_name='newspost',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='auctionitem',
            name='provider',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='fee',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='result',
        ),
        migrations.AddField(
            model_name='auctionitem',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionitem',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.newspost'),
        ),
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='newscategory',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='newspost',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='report',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='report',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='order_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='auctionitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='auctionitem',
            name='price_received',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='auctionitem',
            name='price_start',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='auctionitem',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auction_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppCharitySocialNetwork.comment'),
        ),
        migrations.AlterField(
            model_name='newscategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('man', 'man'), ('women', 'women'), ('other', 'other')], default=0, max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='newscategory',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='newspost',
            unique_together={('title',)},
        ),
        migrations.CreateModel(
            name='HistoryAuction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='AppCharitySocialNetwork.newspost')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['post', 'price', 'user'],
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
        migrations.RemoveField(
            model_name='newspost',
            name='tile',
        ),
        migrations.AddField(
            model_name='newspost',
            name='hashtag',
            field=models.ManyToManyField(blank=True, related_name='news_post', related_query_name='hashtags', to='AppCharitySocialNetwork.Hashtag'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.optionreport'),
        ),
        migrations.CreateModel(
            name='EmotionPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='author', to=settings.AUTH_USER_MODEL)),
                ('emotion_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='emotion_type', to='AppCharitySocialNetwork.emotiontype')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppCharitySocialNetwork.newspost')),
            ],
            options={
                'ordering': ['emotion_type', 'post'],
                'unique_together': {('author', 'post')},
            },
        ),
        migrations.CreateModel(
            name='EmotionComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='author', to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppCharitySocialNetwork.comment')),
                ('emotion_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='emotion_type', to='AppCharitySocialNetwork.emotiontype')),
            ],
            options={
                'ordering': ['emotion_type', 'comment'],
                'unique_together': {('author', 'comment')},
            },
        ),
    ]