from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class ModelBase(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="uploads/")
    description = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True
        ordering = ['id']


class User(AbstractUser):
    typeGender = ((0, 'man'), (1, 'women'), (2, 'other'))

    class Meta:
        ordering = ['id']

    nick_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=255,null=True)
    avatar = models.ImageField(upload_to='uploads/', null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=typeGender, default=0)


class NewsCategory(ModelBase):
    pass

class NewsPost(ModelBase):
    short_description = ModelBase.description
    content = models.TextField()
    tile = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='post',
                             related_query_name='my_post')
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name='category')


class Comment(ModelBase):
    name = None
    image = None
    description = None
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='comment', related_query_name='my_comment', null=True)
    comment_parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    newspost = models.ForeignKey(NewsPost, on_delete=models.CASCADE)



class Report(ModelBase):
    name = None
    image = None
    description = None
    content = models.TextField()
    reason = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='post')


class AuctionItem(ModelBase):
    price_start = models.DecimalField(max_digits=10, decimal_places=2)
    price_received = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='auction_provider')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='auction_receiver')


class Transaction(ModelBase):
    name = None

    amount = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    result = models.DecimalField(max_digits=10, decimal_places=2)
    status = ModelBase.description
    message = models.TextField()
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions')
