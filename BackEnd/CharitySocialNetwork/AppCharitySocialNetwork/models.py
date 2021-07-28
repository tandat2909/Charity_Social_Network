from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class ModelBase(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="uploads/")
    description = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['id']


class User(AbstractUser):
    nickName = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to='uploads/', null=True)

    class Meta:
        ordering = ['id']
