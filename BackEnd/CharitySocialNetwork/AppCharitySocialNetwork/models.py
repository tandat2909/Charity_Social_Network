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
    avatar = models.ImageField(upload_to='images/%y/%M/%d/', null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=typeGender, default=0)
  


class NewsCategory(ModelBase):
    class Meta:
        unique_together = ("name",)
        ordering = ['created_date']


class NewsPost(ModelBase):
    name = None
    content = models.TextField()
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, )
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name='category')
    hashtag = models.ManyToManyField('Hashtag', blank=True)
    is_show = models.BooleanField(default=False, help_text="Chỉ người duyệt bài mới cho phép thay đổi")
    comments = models.ManyToManyField('Comment', blank=True, related_query_name="comments")
    reports = models.ManyToManyField('ReportPost', blank=True, related_query_name="reports")

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ("title",)
    # ordering = ['-created_date']


class Comment(ModelBase):
    name = None
    image = None
    description = None
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_child = models.ManyToManyField('Comment', blank=True)


    def __str__(self):
        return self.content


class OptionReport(models.Model):
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class ReportPost(ModelBase):
    name = None
    description = None
    content = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='post')
    reason = models.ForeignKey(OptionReport, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content


class ReportUser(ModelBase):
    name = None
    description = None
    content = models.TextField()
    user_report = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_report')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.ForeignKey(OptionReport, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.get_full_name() + " => " + self.user_report.get_full_name()


class AuctionItem(ModelBase):
    name = None
    image = None
    description = None
    price_start = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    price_received = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='auction_receiver',
                                 blank=True)
    post = models.ForeignKey(NewsPost, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('post',)

    def __str__(self):
        return str(self.id)


class Transaction(ModelBase):
    name = None
    amount = models.IntegerField()
    message = models.TextField()
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions')
    order_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.order_id + "-" + self.message

    def get_order_id(self):
        return self.order_id

    def get_user(self):
        return self.provider


class EmotionType(ModelBase):
    name = models.CharField(max_length=50, unique=True)


class Emotion(ModelBase):
    image = None
    description = None
    name = None
    emotion_type = models.ForeignKey(EmotionType,
                                     on_delete=models.SET_NULL,
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
    price = models.DecimalField(max_digits=50, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.get_full_name() + " : " + self.post.title + " -> " + str(self.price)

    class Meta:
        ordering = ["post", "price", "user"]
