# Generated by Django 3.2.5 on 2021-09-17 09:59

import ckeditor.fields
import cloudinary.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmotionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
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
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['created_date'],
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('content', ckeditor.fields.RichTextField()),
                ('title', models.CharField(max_length=255)),
                ('is_show', models.BooleanField(default=False, help_text='Ch??? ng?????i duy???t b??i m???i cho ph??p thay ?????i')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post', to='AppCharitySocialNetwork.newscategory')),
                ('hashtag', models.ManyToManyField(blank=True, to='AppCharitySocialNetwork.Hashtag')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Th??ng b??o ng?????i d??ng'), (1, 'Th??ng b??o h??? th??ng'), (2, 'Th??ng b??o b??i vi???t m???i'), (3, 'Th??ng b??o c?? b??i vi???t ?????u gi??'), (4, 'Report')], default=0, help_text='Ch???n lo???i th??ng b??o')),
                ('url', models.CharField(max_length=255, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='OptionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nick_name', models.CharField(max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('avatar', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='avatar')),
                ('birthday', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('man', 'man'), ('women', 'women'), ('other', 'other')], default=0, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('amount', models.IntegerField()),
                ('message', models.TextField()),
                ('order_id', models.CharField(max_length=255, null=True)),
                ('provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReportUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('reason', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.optionreport')),
                ('user', models.ForeignKey(help_text='Ch???n user cho h??nh ?????ng', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('user_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_report', related_query_name='user_report', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReportPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.newspost')),
                ('reason', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.optionreport')),
                ('user', models.ForeignKey(help_text='Ch???n user cho h??nh ?????ng', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newspost',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='HistoryAuction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=50)),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='historyauction', to='AppCharitySocialNetwork.newspost')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['post', 'price', 'user'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('comment_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_child', to='AppCharitySocialNetwork.comment')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.newspost')),
                ('user', models.ForeignKey(help_text='Ch???n user cho h??nh ?????ng', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NotificationUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('notification', models.ForeignKey(help_text='Ch???n th??ng b??o cho ng?????i d??ng', on_delete=django.db.models.deletion.CASCADE, related_name='notification_users', to='AppCharitySocialNetwork.notification')),
                ('user', models.ForeignKey(help_text='Ch???n ng?????i d??ng c???n th??ng b??o', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date', 'new'],
                'unique_together': {('user', 'notification')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='newspost',
            unique_together={('title',)},
        ),
        migrations.CreateModel(
            name='EmotionPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.newspost')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.emotiontype')),
                ('user', models.ForeignKey(help_text='Ch???n user cho h??nh ?????ng', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('post', 'user')},
            },
        ),
        migrations.CreateModel(
            name='EmotionComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emotions_comment', related_query_name='emotions_comment', to='AppCharitySocialNetwork.comment')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppCharitySocialNetwork.emotiontype')),
                ('user', models.ForeignKey(help_text='Ch???n user cho h??nh ?????ng', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'comment')},
            },
        ),
        migrations.CreateModel(
            name='AuctionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('price_start', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('price_received', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=50)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('post', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='info_auction', to='AppCharitySocialNetwork.newspost')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('post',)},
            },
        ),
    ]
