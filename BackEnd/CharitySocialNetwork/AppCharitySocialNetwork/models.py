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
    is_show = models.BooleanField(default=False, help_text="Chỉ người duyệt bài mới cho phép thay đổi")

    # comments = models.ManyToManyField('Comment', blank=True, related_query_name="comments")
    # reports = models.ManyToManyField('ReportPost', blank=True, related_query_name="reports")
    # emotions = models.ManyToManyField("EmotionPost", blank=True, related_query_name="emotions")

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ("title", "user")

        # ordering = ['-created_date']


class AuctionItem(ModelBase):
    UNPAID, NOT_YET_SHIPPED, SHIPPING, SHIPPED, REFUND = range(5)

    status = models.SmallIntegerField(choices=settings.STATUS_AUCTION_ITEM,default=UNPAID,null=False)
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
        return self

    def is_paid(self):
        try:
                    # trường hợp đã ghi nhận thanh toán mà chưa chuyển trạng thái
            return self.UNPAID == self.status and self.transaction.status == Transaction.COMPLETED \
                    or self.status != self.UNPAID  # khác trường hợp này thì auction đã thanh toán
        except:
            return False

    @property
    def status_str(self):
        if self.UNPAID == self.status and self.transaction.status == Transaction.COMPLETED:
            return "PAID"
        return settings.STATUS_AUCTION_ITEM[self.status][1]


class EmotionType(ModelBase):
    name = models.CharField(max_length=50, unique=True)


class ActionBase(ModelBase):
    description = None
    name = None
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False,
                             help_text="Chọn user cho hành động")
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
        unique_together = ('post', "user")  # một user chỉ thả 1 cảm súc trên một bài


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
        return 'Nội dung Report:\n' \
               'Bài viết: {title} \n' \
               'Lý do:{reason}\n' \
               'Nội dung: {content}\n' \
               'Ngày: {date}\n' \
            .format(title=self.post.title, reason=self.reason, content=self.content, date=self.created_date)


class ReportUser(ActionBase):
    post = None
    content = models.TextField()
    user_report = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_report',
                                    related_query_name="user_report")
    reason = models.ForeignKey(OptionReport, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Nội dung Report:\n' \
               'User bị report: {fullname} \n' \
               'Lý do:{reason}\n' \
               'Nội dung: {content}\n' \
               'Ngày: {date}\n' \
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
#         return 'Nội dung Report:\n' \
#                'Bài viết: {title} \n' \
#                'Lý do:{reason}\n' \
#                'Nội dung: {content}\n' \
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
#         return 'Nội dung Report:\n' \
#                'User: {fullname} \n' \
#                'Lý do:{reason}\n' \
#                'Nội dung: {content}\n' \
#             .format(fullname=self.user.get_full_name() or self.user.username, reason=self.reason.content,
#                     content=self.content)


class Transaction(ModelBase):
    name = None
    PENDING, COMPLETED = range(2)
    status_code = settings.STATUS_PAYMENT
    amount = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    message = models.TextField(null=True, blank=True)
    # seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='seller',
    #                            help_text="Thông tin người bán")
    order_id = models.CharField(max_length=255, null=True, blank=True, help_text="Có mới lưu mã hóa đơn của paypal")
    # buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name="buyer",
    #                           help_text="Thông tin người mua")
    status = models.SmallIntegerField(choices=status_code, default=0,
                                      help_text='Trạng thái mặc định của hóa đơn là chưa hoàn thành')
    currency_code = models.CharField(max_length=10, null=False, blank=False, help_text="Yêu cầu nhập mã loại tiền tệ")
    auction_item = models.OneToOneField(AuctionItem, on_delete=models.SET_NULL, null=True, related_name="transaction",
                                        help_text="Mã bài viết không được để trống")
    created_date = models.DateTimeField()
    update_date = models.DateTimeField()

    def __str__(self):
        info = "Mã hóa đơn: {order_id}\n" \
               "Sản phẩm: {title}\n" \
               "Giá: {amount} {currency_code}\n" \
               "Ngày thanh toán: {created_date} \n" \
               "Trạng thái: {status}".\
            format(
            order_id=self.order_id,
            title=self.message,
            amount= self.amount,
            currency_code=self.currency_code,
            created_date=self.created_date,
            status=settings.STATUS_PAYMENT[self.status][1]
        )
        return info


    def get_order_id(self):
        return self.order_id

    def get_buyer(self):
        return self.auction_item.receiver

    def get_seller(self):
        return self.auction_item.post.user


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
#     # một tài khoản có thể like nhiều bài viết mà mỗi bài viết chỉ like một lần
#     # lấy tất cả các like của bài viết a
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
    Muốn thông báo danh riêng cho user thì khi tạo thông báo add vào bảng NotificationUser
    Muốn lấy thông báo hệ thông và thông báo user queryset = Notification.objects.filter(notification_users__user_id = user_id,type = Notification.SYSTEM)
"""


class Notification(models.Model):
    SYSTEM, POST, POST_AUCTION, PRICE_NEW, REPORT = range(5)
    type_notification = settings.TYPE_NOTIFICATION
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(choices=type_notification, default=0, help_text="Chọn loại thông báo")
    new = models.BooleanField(default=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False,
                             help_text="Chọn người dùng cần thông báo", related_name="notifications")

    class Meta:
        ordering = ["-created_date"]
        # unique_together = ("user", "id")

# class NotificationUser(models.Model):
#     notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=False, blank=False,
#                                      help_text="Chọn thông báo cho người dùng", related_name="users")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
#                              help_text="Chọn người dùng cần thông báo",related_name="notifications")
#     # url = models.CharField(max_length=255)
#     new = models.BooleanField(default=True)
#     active = models.BooleanField(default=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ["-created_date", "new"]
#         unique_together = ("user", "notification")
