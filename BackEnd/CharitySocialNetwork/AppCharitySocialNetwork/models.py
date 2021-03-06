import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from django.conf import settings


# Create your models here.


class ModelBase(models.Model):
    name = models.CharField(max_length=255)
    image = CloudinaryField('image', null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['id']

    def __str__(self):
        return self.name or ""

    @property
    def get_url_image(self):
        return self.image.url


class User(AbstractUser):
    typeGender = (("man", 'man'), ("women", 'women'), ("other", 'other'))

    class Meta:
        ordering = ['id']

    nick_name = models.CharField(max_length=255, null=True, )
    phone_number = models.CharField(max_length=20, null=True, )
    address = models.CharField(max_length=255, null=True)
    avatar = CloudinaryField('avatar', null=True, blank=False)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=typeGender, default=0)

    # notifications = models.ManyToManyField('Notification', blank=True)

    @property
    def get_url_image(self):
        return self.avatar.url


class NewsCategory(ModelBase):
    class Meta:
        unique_together = ("name",)
        ordering = ['created_date']


class NewsPost(ModelBase):
    name = None
    description = models.TextField()
    content = RichTextField(null=False)
    title = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="posts")
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    hashtag = models.ManyToManyField('Hashtag', blank=True)
    is_show = models.BooleanField(default=False, help_text="Ch??? ng?????i duy???t b??i m???i cho ph??p thay ?????i")

    # comments = models.ManyToManyField('Comment', blank=True, related_query_name="comments")
    # reports = models.ManyToManyField('ReportPost', blank=True, related_query_name="reports")
    # emotions = models.ManyToManyField("EmotionPost", blank=True, related_query_name="emotions")

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ("title", "user")

        # ordering = ['-created_date']


class AuctionItem(ModelBase):
    name = None
    image = None
    description = None
    price_start = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    price_received = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 blank=True)
    post = models.OneToOneField(NewsPost, on_delete=models.SET_NULL, null=True, blank=True, related_name="info_auction")

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    class Meta:
        unique_together = ('post',)

    def __str__(self):
        return str(self.id)


class EmotionType(ModelBase):
    name = models.CharField(max_length=50, unique=True)


class ActionBase(ModelBase):
    description = None
    name = None
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False,
                             help_text="Ch???n user cho h??nh ?????ng")
    post = models.ForeignKey(NewsPost, on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        abstract = True
        ordering = ['id']


class Comment(ActionBase):
    content = models.TextField()
    comment_parent = models.ForeignKey("Comment", on_delete=models.CASCADE, blank=True, null=True,
                                       related_name="comment_child")

    def __str__(self):
        return self.content


class EmotionsBase(ActionBase):
    image = None
    type = models.ForeignKey(EmotionType, on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        abstract = True


class EmotionPost(EmotionsBase):
    class Meta:
        unique_together = ('post', "user")  # m???t user ch??? th??? 1 c???m s??c tr??n m???t b??i


class EmotionComment(EmotionsBase):
    post = None
    comment = models.ForeignKey(Comment, verbose_name="comment", on_delete=models.SET_NULL, null=True, blank=False,
                                related_name="emotions_comment", related_query_name="emotions_comment")

    class Meta:
        unique_together = ('user', "comment")


class OptionReport(models.Model):
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class ReportPost(ActionBase):
    content = models.TextField(null=True, blank=True)
    reason = models.ForeignKey(OptionReport, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'N???i dung Report:\n' \
               'B??i vi???t: {title} \n' \
               'L?? do:{reason}\n' \
               'N???i dung: {content}\n' \
               'Ng??y: {date}\n' \
            .format(title=self.post.title, reason=self.reason, content=self.content, date=self.created_date)


class ReportUser(ActionBase):
    post = None
    content = models.TextField()
    user_report = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_report',
                                    related_query_name="user_report")
    reason = models.ForeignKey(OptionReport, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'N???i dung Report:\n' \
               'User b??? report: {fullname} \n' \
               'L?? do:{reason}\n' \
               'N???i dung: {content}\n' \
               'Ng??y: {date}\n' \
            .format(fullname=self.user.get_full_name() or self.user.username, reason=self.reason.content,
                    content=self.content, date=self.created_date)


#
# class Comment(ModelBase):
#     name = None
#     image = None
#     description = None
#     content = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     comment_child = models.ManyToManyField('Comment', blank=True)
#     emotions = models.ManyToManyField("EmotionComment", blank=True, related_query_name="emotions")
#
#     def __str__(self):
#         return self.content

#
# class OptionReport(models.Model):
#     content = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.content
#
#
# class ReportPost(ModelBase):
#     name = None
#     description = None
#     content = models.TextField(null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
#     post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='post')
#     reason = models.ForeignKey(OptionReport, on_delete=models.SET_NULL, null=True)
#
#     def __str__(self):
#         return 'N???i dung Report:\n' \
#                'B??i vi???t: {title} \n' \
#                'L?? do:{reason}\n' \
#                'N???i dung: {content}\n' \
#             .format(title=self.post.title, reason=self.reason, content=self.content)
#
#
# class ReportUser(ModelBase):
#     name = None
#     description = None
#     content = models.TextField()
#     user_report = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_report')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     reason = models.ForeignKey(OptionReport, on_delete=models.SET_NULL, null=True)
#
#     def __str__(self):
#         return 'N???i dung Report:\n' \
#                'User: {fullname} \n' \
#                'L?? do:{reason}\n' \
#                'N???i dung: {content}\n' \
#             .format(fullname=self.user.get_full_name() or self.user.username, reason=self.reason.content,
#                     content=self.content)


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


#
# class Emotion(ModelBase):
#     image = None
#     description = None
#     name = None
#     emotion_type = models.ForeignKey(EmotionType,
#                                      on_delete=models.SET_NULL,
#                                      null=True,
#
#                                      )
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name='author')
#
#     # m???t t??i kho???n c?? th??? like nhi???u b??i vi???t m?? m???i b??i vi???t ch??? like m???t l???n
#     # l???y t???t c??? c??c like c???a b??i vi???t a
#     class Meta:
#         abstract = True
#
#     def __str__(self):
#         return self.author.get_username() + " : " + self.author.get_full_name() + " -> " + self.emotion_type.name
#
#
# class EmotionPost(Emotion):
#     post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name="emotion")
#
#     class Meta:
#         ordering = ['emotion_type', "post"]
#         unique_together = ("author", "post")
#
#
# class EmotionComment(Emotion):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#
#     class Meta:
#         ordering = ["emotion_type", "comment"]
#         unique_together = ("author", "comment")


class Hashtag(ModelBase):
    image = None

    class Meta:
        unique_together = ("name",)


class HistoryAuction(ModelBase):
    name = None
    image = None
    price = models.DecimalField(max_digits=50, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, default=None, related_name="historyauction")

    def __str__(self):
        return str(self.user) + " : " + self.post.title + " -> " + str(self.price)

    class Meta:
        ordering = ["post", "price", "user"]


"""
    Mu???n th??ng b??o danh ri??ng cho user th?? khi t???o th??ng b??o add v??o b???ng NotificationUser
    Mu???n l???y th??ng b??o h??? th??ng v?? th??ng b??o user queryset = Notification.objects.filter(notification_users__user_id = user_id,type = Notification.SYSTEM)
"""


class Notification(models.Model):
    SYSTEM, POST, POST_AUCTION, PRICE_NEW, REPORT = range(5)
    type_notification = settings.TYPE_NOTIFICATION
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(choices=type_notification, default=0, help_text="Ch???n lo???i th??ng b??o")
    new = models.BooleanField(default=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False,
                             help_text="Ch???n ng?????i d??ng c???n th??ng b??o", related_name="notifications")

    class Meta:
        ordering = ["-created_date"]
        # unique_together = ("user", "id")

# class NotificationUser(models.Model):
#     notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=False, blank=False,
#                                      help_text="Ch???n th??ng b??o cho ng?????i d??ng", related_name="users")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
#                              help_text="Ch???n ng?????i d??ng c???n th??ng b??o",related_name="notifications")
#     # url = models.CharField(max_length=255)
#     new = models.BooleanField(default=True)
#     active = models.BooleanField(default=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ["-created_date", "new"]
#         unique_together = ("user", "notification")
