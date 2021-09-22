from django.contrib.auth.models import Group
from graphene import Scalar, String
from graphene_django import converter
from graphql import GraphQLError

from .models import *
from graphene_django import *


class CloudinaryUrl(Scalar):
    """
        The `CloudinaryUrl` conver instance `CloudinaryField` to url of server Cloudinary
    """

    @staticmethod
    def coerce_to_url(value):
        # print(type(value))
        return value.url

    serialize = coerce_to_url
    parse_value = coerce_to_url
    parse_literal = coerce_to_url


@converter.convert_django_field.register(CloudinaryField)
def convert_cloudinary_field_to_string(field, registry=None):
    """
        Đăng ký chuyển đổi CloudinaryField sang url string
        Nói cho graphene_django biết chuyển đổi field dữ liệu đó như thế nào

    """
    return CloudinaryUrl(description=field.help_text, required=not field.null)


class BaseMeta:
    model = None
    fields = '__all__'
    exclude = None


class AccountObjectType(DjangoObjectType):
    full_name = String()

    class Meta(BaseMeta):
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'nick_name', 'birthday', 'phone_number', 'gender',
                  'email',
                  'avatar', 'address', 'date_joined', 'last_login', 'posts', 'notifications', 'historyauction_set',
                  'auctionitem_set',
                  ]

    # Thông thường đối số đầu tiên cho phương thức này sẽ là `self`,
    # nhưng Graphene thực thi điều này như một staticmethod ngầm.
    # => Nếu hàm resolver không chỉ định nó là @staticmethod thì nó ngầm định sẽ thực hiện hàm nó như một staticmethod
    # và tham số đầu tiên của hàm như một biến bình thường và giá trị của nó bằng None
    def resolve_full_name(self, info):
        return self.first_name + " " + self.last_name


class PostObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = NewsPost
        fields = ['id', 'content', 'title', 'is_show', 'created_date', 'update_date', 'description',
                  'user', 'hashtag', 'info_auction', 'comment_set', 'emotionpost_set', 'historyauction',
                  ]

    def resolve_is_show(self, info):
        if info.context.user.is_authenticated:
            return self.is_show
        raise GraphQLError("Bạn không có quyền xem trường thông tin này")

    def resolve_comment_set(self, info):
        return self.comment_set.filter(active=True, comment_parent=None)

    def resolve_historyauction(self, info):
        user_post = self.user
        user = info.context.user
        if user.is_authenticated:
            if user.pk == user_post.pk or user.is_superuser:
                return self.historyauction.filter(active=True)
        return self.historyauction.filter(active=True, user_id=user.pk)


class AuctionItemObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = AuctionItem
        fields = [
            'id',
            'price_start',
            'price_received',
            'receiver',
            'post',
            'start_datetime',
            'end_datetime',
        ]


class HistoryAuctionObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = HistoryAuction
        fields = [
            'id',
            'price',
            'created_date',
            'description',
            'post',
            'update_date',
            'user'
        ]


class ReportPostObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = ReportPost


class ReportUserObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = ReportUser


class OptionsReportObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = OptionReport


class HashtagObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = Hashtag
        fields = ['id', 'name', 'newspost_set', ]


class CommentObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = Comment
        fields = ['id', 'content', 'image', 'emotions_comment', 'created_date', 'update_date', 'comment_child', 'user']


# Emotion làm lại database chỉ cần một emotion làm hết
class EmotionsTypeObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = EmotionType
        fields = ['id', 'image', 'description', 'name']


class EmotionsPostObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = EmotionPost
        fields = ['id', 'created_date', 'update_date', 'user', 'type', ]


class EmotionsCommentObjectType(DjangoObjectType):
    class Meta(BaseMeta):
        model = EmotionComment
        fields = ['id', 'created_date', 'update_date', 'user', 'type', ]


class NotificationObjectsType(DjangoObjectType):
    class Meta(BaseMeta):
        model = Notification
        fields = ["id", "title", "message", "type", "new", "created_date", "url"]


class GroupObjectsType(DjangoObjectType):
    class Meta(BaseMeta):
        model = Group
