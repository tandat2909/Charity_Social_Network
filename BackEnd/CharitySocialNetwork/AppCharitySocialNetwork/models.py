from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class ModelBase(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['id']

    def __str__(self):
        return self.name


class User(AbstractUser):
    typeGender = (("man", 'man'), ("women", 'women'), ("other", 'other'))

    class Meta:
        ordering = ['id']

    nick_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to='uploads/', null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=typeGender, default=0)


class NewsCategory(ModelBase):
    class Meta:
        unique_together = ("name",)


class NewsPost(ModelBase):
    name = None
    content = models.TextField()
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, )
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name='category')
    hashtag = models.ManyToManyField('Hashtag', related_name='news_post', related_query_name='hashtags', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ("title",)


class Comment(ModelBase):
    name = None
    image = None
    description = None
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='comment', related_query_name='my_comment', null=True)
    comment_parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    newspost = models.ForeignKey(NewsPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class OptionReport(models.Model):
    content = models.CharField(max_length=255)


class Report(ModelBase):
    name = None
    description = None
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='post')
    reason = models.ForeignKey(OptionReport, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content


class AuctionItem(ModelBase):
    price_start = models.DecimalField(max_digits=10, decimal_places=2)
    price_received = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='auction_provider')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='auction_receiver',
                                 blank=True)


class Transaction(ModelBase):
    name = None
    amount = models.IntegerField()
    message = models.TextField()
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions')
    order_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.order_id + "-" + self.message


class EmotionType(ModelBase):
    name = models.CharField(max_length=50, unique=True)


class Emotion(ModelBase):
    image = None
    description = None
    name = None
    emotion_type = models.ForeignKey(EmotionType,
                                     on_delete=models.SET_NULL,
                                     related_query_name="emotion_type",
                                     null=True,

                                     )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name='author')

    # một tài khoản có thể like nhiều bài viết mà mỗi bài viết chỉ like một lần
    # lấy tất cả các like của bài viết a
    class Meta:
        abstract = True

    def __str__(self):
        return self.author.get_username() + " : " + self.author.get_full_name() + " -> " + self.emotion_type.name


class EmotionPost(Emotion):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)

    class Meta:
        ordering = ['emotion_type', "post"]
        unique_together = ("author", "post")


class EmotionComment(Emotion):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        ordering = ["emotion_type", "comment"]
        unique_together = ("author", "comment")


class Hashtag(ModelBase):
    image = None

    class Meta:
        unique_together = ("name",)


class HistoryAuction(ModelBase):
    name = None
    image = None
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() + " : " + self.item.name + " -> " + str(self.price)

    class Meta:
        ordering = ["item", "price", "user"]
