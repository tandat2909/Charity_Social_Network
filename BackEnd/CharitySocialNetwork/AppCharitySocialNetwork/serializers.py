import rest_framework.exceptions
from cloudinary import CloudinaryResource, models as cloudmodels
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import *
from django.contrib.auth.models import Group, Permission
from .models import *
from .validators import PasswordValidator


class BaseMeta:
    '''
     valid_kwargs = {
                'read_only', 'write_only',
                'required', 'default', 'initial', 'source',
                'label', 'help_text', 'style',
                'error_messages', 'validators', 'allow_null', 'allow_blank',
                'choices'
            }
    '''
    fields = '__all__' or ['id', ]
    model = ""
    filter = []
    exclude = None
    read_only_fields = None
    extra_kwargs = {}


# User
class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class GroupsSerializer(ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class UserViewModelSerializer(ModelSerializer):
    avatar = ImageField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']
        read_only_fields = ['id', 'username', 'first_name', 'last_name', 'avatar']

    # def get_avatar(self, obj):
    #     return obj.avatar.url or ""


class UserSerializer(ModelSerializer):
    avatar = ImageField(required=True, error_messages={'required': 'Avatar không được để trống'})

    class Meta(BaseMeta):
        model = User
        fields = None
        exclude = ['password', 'is_superuser', 'is_active', 'is_staff', 'last_login', 'groups', 'user_permissions']
        read_only_fields = ["date_joined", 'id']

    #
    # def get_avatar(self, obj):
    #     return obj.avatar.url
    # def validate(self, attrs):
    #     print(type(attrs.get('avatar', None)))
    #     return attrs


class UserRegisterSerializer(ModelSerializer):
    avatar = ImageField(required=True, error_messages={'required': 'Avatar không được để trống'})

    class Meta(BaseMeta):
        model = User
        fields = None
        exclude = ['is_superuser', 'is_staff', 'last_login', 'is_active', 'groups', 'user_permissions', 'notifications']
        read_only_fields = ["date_joined", 'id']
        extra_kwargs = {
            'password': {
                'write_only': True,
                "validators": [PasswordValidator(language="VN"), ],
                'style': {'input_type': 'password'}
            },
        }

    # def validate(self, attrs):
    #     if not attrs.get("avatar", None):
    #         raise rest_framework.exceptions.ValidationError({'avatar': "Yêu cầu cung cấp hình ảnh đại diện"})
    #     return attrs

    def create(self, validated_data):
        # avatar = validated_data.get("avatar", None)
        # print(type(avatar))
        u = User(**validated_data)
        u.set_password(u.password)
        u.save()
        # print(u.avatar.url)
        return self.add_group_permission(user=u)

    def add_group_permission(self, user):
        grs = Group.objects.filter(name='User').first()
        user.groups.add(grs)
        user.save()
        return user


class UserChangePasswordSerializer(ModelSerializer):
    password_new = CharField(max_length=40, min_length=8, required=True,
                             validators=[PasswordValidator(language='VN'), ], )

    password_confirm = CharField(max_length=40, min_length=8, required=True)

    class Meta:
        model = User
        fields = ["password", 'password_new', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_new': {'write_only': True},
            'password_confirm': {'write_only': True},
        }

    def validate(self, attrs):

        if not attrs["password_new"].__eq__(attrs["password_confirm"]):
            raise ValidationError({"Error": "Password confirm invalid"})
        return attrs

    def update(self, instance, validated_data):
        if instance.check_password(validated_data["password"]):
            if instance.check_password(validated_data["password_new"]):
                raise ValidationError({'Error': "The new password is the same as the old password"})
            instance.set_password(validated_data["password_new"])
            instance.save()
            return instance
        raise ValidationError({'Error': "password invalid"})


# end User

# Emotion

class EmotionTypeSerializer(ModelSerializer):
    image = ImageField()

    class Meta(BaseMeta):
        model = EmotionType
        fields = ['id', 'name', 'image', 'description', ]


class EmotionStatisticalSerializer(EmotionTypeSerializer):
    amount = IntegerField(default=0)

    class Meta(EmotionTypeSerializer.Meta):
        fields = EmotionTypeSerializer.Meta.fields + ['amount', ]
        extra_kwargs = {
            'amount': {"read_only": True},
        }


class EmotionCommentSerializer(ModelSerializer):
    author = UserViewModelSerializer()

    class Meta(BaseMeta):
        model = EmotionComment
        extra_kwargs = {
            'comment': {"write_only": True},
            'active': {"write_only": True}
        }


class EmotionPostSerializer(ModelSerializer):
    author = UserViewModelSerializer()

    class Meta(BaseMeta):
        model = EmotionPost
        extra_kwargs = {
            'post': {"write_only": True},
            'active': {"write_only": True}
        }


# end Emotion

# Post
class CategoryPostSerializer(ModelSerializer):
    image = ImageField()

    class Meta:
        model = NewsCategory
        fields = ["id", "name", 'image', 'description']


class HashtagsSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'description']


class AuctionItemModelSerializer(ModelSerializer):
    # YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]
    class Meta(BaseMeta):
        model = AuctionItem
        fields = ["id", "post", "price_start", 'start_datetime', 'end_datetime']
        extra_kwargs = {
            "id": {"read_only": True}
        }

    def validate(self, attrs):
        if attrs["start_datetime"].__ge__(attrs["end_datetime"]):
            raise rest_framework.exceptions.ValidationError({
                "end_datetime": "Thời gian kết thúc phải lớn hơn thời gian bắt đầu"
            })
        return attrs


class AuctionItemSerializer(ModelSerializer):
    class Meta:
        model = AuctionItem
        fields = ["id", "price_start", 'price_received', 'receiver', 'start_datetime', 'end_datetime']


class PostSerializer(ModelSerializer):
    user = UserViewModelSerializer()
    category = CategoryPostSerializer()
    hashtag = HashtagsSerializer(many=True)
    info_auction = AuctionItemSerializer(many=True)
    image = ImageField()

    class Meta(BaseMeta):
        model = NewsPost
        fields = None
        exclude = ["reports"]
        extra_kwargs = {
            'active': {'write_only': True},
            'is_show': {'write_only': True},
            'id': {'read_only': True},
        }


class HistoryAuctionSerializer(ModelSerializer):
    user = UserViewModelSerializer(required=False)

    class Meta(BaseMeta):
        model = HistoryAuction
        fields = ["id", "price", "user", 'description']
        extra_kwargs = {
            "user": {"read_only": True}
        }


class HistoryAuctionCreateSerializer(ModelSerializer):
    class Meta:
        model = HistoryAuction
        fields = ["id", "price", "user", 'description', 'post']

    def create(self, validated_data):
        pass


class PostListSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = NewsPost
        exclude = ["comments", "active", "is_show"] + PostSerializer.Meta.exclude


class PostDetailSerializer(PostSerializer):
    historyauction = HistoryAuctionSerializer(many=True)

    class Meta(PostSerializer.Meta):
        extra_kwargs = {**PostSerializer.Meta.extra_kwargs,
                        "history_auction": {"read_only": True}
                        }


class PostCreateSerializer(ModelSerializer):
    hashtag = ListSerializer(child=CharField(required=False, max_length=100), required=False)
    price_start = DecimalField(required=False, max_digits=50, decimal_places=2)
    # YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]
    start_datetime = DateTimeField(required=False)
    end_datetime = DateTimeField(required=False)

    class Meta:
        model = NewsPost
        fields = ["id", "category", "hashtag", "description", "content", "title", 'price_start', "user", 'image',
                  'start_datetime', 'end_datetime']
        read_only_fields = ["user", ]
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def valid_start_datetime(self, date):
        # print("valid_start_datetime", date, date.timestamp(), datetime.datetime.now().timestamp(), type(date),
        #       type(datetime.datetime.now()))

        if date.timestamp() >= datetime.datetime.now().timestamp():
            return True
        raise ValidationError({"start_date": "Ngày bắt đầu phải lớn hơn hoặc bằng ngày hiện tại"})

    def valid_end_datetime(self, date, **kwargs):
        start_datetime = kwargs.get('start_datetime', datetime.datetime.now())
        end_datetime = date
        if self.valid_start_datetime(start_datetime) and end_datetime.timestamp() >= start_datetime.timestamp():
            return True
        raise ValidationError({"end_date": "thời gian kết thúc phải lớn hơn hoặc bằng thời gian bắt đầu"})

    def add_hashtag(self, post, hashtags, **kwargs):
        action = kwargs.get("action", 'create')
        if hashtags:
            if not type(hashtags) is list:
                raise rest_framework.exceptions.ValidationError(
                    {"hashtag": "yêu cầu một danh sách các hash tag không phải một chuỗi"})
            for item in hashtags:
                instance_hashtag, create = Hashtag.objects.get_or_create(name=item)
                if not create and action == 'update':
                    continue
                instance_hashtag, create = Hashtag.objects.get_or_create(name=item)
                post.hashtag.add(instance_hashtag)

    def create(self, validated_data, **kwargs):

        data_auction = {
            "price_start": validated_data.pop("price_start", None),
            'start_datetime': validated_data.pop("start_datetime", None),
            'end_datetime': validated_data.pop("end_datetime", None)
        }
        if validated_data.get("category", None) is None:
            raise rest_framework.exceptions.ValidationError({"Category": "fields not empty"})

        # print(data_auction)
        hashtag = validated_data.pop("hashtag", None)
        instance_news_post = super().create(validated_data)

        self.add_hashtag(instance_news_post, hashtag)

        # kiểm tra bài viết có phải là danh mục đấu giá không
        if instance_news_post.category.id == settings.CATEGORY_POST_AUCTION:
            data_auction["post"] = instance_news_post.id
            try:
                serializer_auction = AuctionItemModelSerializer(data=data_auction)
                serializer_auction.is_valid(raise_exception=True)
                serializer_auction.save()
            except Exception as ex:
                instance_news_post.delete()
                raise ex
        return instance_news_post

    def update(self, instance, validated_data):
        """
            update cập nhật hashtag hoặc tạo mới
            cập nhật phần đấu giá kiểm tra nó có phải bài đấu giá không
            không cho cập nhật ngày bắt đầu bé hơn ngày kết thúc và ngày hiện tại

        :param instance:
        :param validated_data:
        :return:
        """
        fields_auction = ["price_start", 'start_datetime', 'end_datetime']
        is_update_auction_post = True if True in [field in validated_data.keys() for field in
                                                  fields_auction] else False
        # print(is_update_auction_post)
        if is_update_auction_post:
            if instance.category.id == settings.CATEGORY_POST_AUCTION:
                try:
                    start_datetime = validated_data.pop("start_datetime", None)
                    end_datetime = validated_data.pop("end_datetime", None)

                    instance_auction_item = AuctionItem.objects.get(post=instance)
                    if start_datetime and self.valid_start_datetime(start_datetime):
                        instance_auction_item.start_datetime = start_datetime or instance_auction_item.start_datetime

                    if end_datetime and self.valid_end_datetime(start_datetime=instance_auction_item.start_datetime,
                                                                date=end_datetime):
                        instance_auction_item.end_datetime = end_datetime or instance_auction_item.end_datetime
                    instance_auction_item.price_start = validated_data.get("price_start",
                                                                           instance_auction_item.price_start)
                    instance_auction_item.save()
                except AuctionItem.DoesNotExist:
                    raise Exception({'error': "Cập nhật thất bại, Đây không phải loại bài viết đấu giá"})
            else:
                raise Exception({'error': "Cập nhật thất bại, Đây không phải loại bài viết đấu giá"})
        # print("update serializer: ", validated_data)
        hashtag = validated_data.pop("hashtag", None)
        # print("update serializer: hashtag: ", hashtag)
        self.add_hashtag(instance, hashtag, action='update')
        return super().update(instance, validated_data)


class PostChangeFieldIsShow(ModelSerializer):
    class Meta:
        model = NewsPost
        fields = ["is_show", ]


# end Post

# Comment

class CommentChildSerializer(ModelSerializer):
    user = UserViewModelSerializer()
    emotions = EmotionCommentSerializer(many=True)

    class Meta:
        model = Comment
        exclude = ['active', ]


class CommentSerializer(ModelSerializer):
    user = UserViewModelSerializer()
    comment_child = CommentChildSerializer(many=True)
    emotions = EmotionCommentSerializer(many=True)

    class Meta:
        model = Comment
        exclude = ['active', ]
        extra_kwargs = {
            'comment_child': {"write_only": True}
        }


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']
        read_only_fields = ['id', ]

    # def create(self, validated_data, **kwargs):
    #     data = {**validated_data, **kwargs}
    #     comment = Comment(**data)
    #     comment.save()
    #     return comment


# end Comment

class OptionReportSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = OptionReport
        filter = None


class ReportPostSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = ReportPost


class ReportPostCreateSerializer(ModelSerializer):
    class Meta:
        model = ReportPost
        exclude = ["post", "user", 'active']
        read_only_fields = ['id', ]

    def validate(self, data):
        if data.get("reason", None) is None:
            raise ValidationError({"reason": "field cannot be empty"})
        return data


class ReportUserSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = ReportUser


class ReportUserCreateSerializer(ModelSerializer):
    class Meta:
        model = ReportUser
        exclude = ["user", 'active']
        read_only_fields = ['id', ]

    def validate(self, data):
        if data.get("reason", None) is None:
            raise ValidationError({"reason": "field cannot be empty"})
        return data


class NotificationSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = Notification
