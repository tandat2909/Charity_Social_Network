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
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']
        read_only_fields = ['id', 'username', 'first_name', 'last_name', 'avatar']


class UserSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = User
        fields = None
        exclude = ['password', 'is_superuser', 'is_staff', 'last_login', 'groups', 'user_permissions']
        read_only_fields = ["date_joined", "is_active", 'id']


class UserRegisterSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = User
        fields = None
        exclude = ['is_superuser', 'is_staff', 'last_login', 'groups', 'user_permissions']
        read_only_fields = ["date_joined", "is_active", 'id']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        u = User(**validated_data)
        u.set_password(u.password)
        u.save()
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

# Post
class CategoryPostSerializer(ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "name"]


class HashtagsSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'description']


class AuctionItemModelSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = AuctionItem
        fields = ["id", "post", "price_start"]
        extra_kwargs = {
            "id": {"read_only": True}
        }


class AuctionItemSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = AuctionItem


class PostSerializer(ModelSerializer):
    user = UserViewModelSerializer()
    category = CategoryPostSerializer()
    hashtag = HashtagsSerializer(many=True)

    class Meta(BaseMeta):
        model = NewsPost
        fields = None
        exclude = ["reports"]
        extra_kwargs = {
            'active': {'write_only': True},
            'is_show': {'write_only': True},
            'id': {'read_only': True},
        }


class PostListSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = NewsPost
        exclude = ["comments", "active", "is_show"] + PostSerializer.Meta.exclude


class PostCreateSerializer(ModelSerializer):
    price_start = DecimalField(required=False, max_digits=50, decimal_places=2)

    class Meta:
        model = NewsPost
        fields = ["id", "category", "hashtag", "description", "content", "title", 'price_start', "user", 'image']
        read_only_fields = ["user", ]
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data, **kwargs):

        data_auction = {"price_start": validated_data.pop("price_start", None)}
        # print(data_auction)
        if data_auction.get("price_start", None):
            instance_news_post = super().create(validated_data)
            data_auction["post"] = instance_news_post.id
            try:
                serializer_auction = AuctionItemModelSerializer(data=data_auction)
                serializer_auction.is_valid(raise_exception=True)
                serializer_auction.save()
            except Exception as ex:
                instance_news_post.delete()
                raise ex
            return instance_news_post

        return super().create(validated_data)

    def update(self, instance, validated_data):
        price_start = validated_data.pop("price_start", None)
        if price_start is not None:
            ai = AuctionItem.objects.get(post_id=instance.id)
            ai.price_start = price_start
            ai.save()
        return super().update(instance, validated_data)


class PostChangeFieldIsShow(ModelSerializer):
    class Meta:
        model = NewsPost
        fields = ["is_show", ]


# end Post

# Comment

class CommentChildSerializer(ModelSerializer):
    user = UserViewModelSerializer()

    class Meta:
        model = Comment
        exclude = ['active', ]


class CommentSerializer(ModelSerializer):
    user = UserViewModelSerializer()
    comment_child = CommentChildSerializer(many=True)

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

# Emotion


class EmotionTypeSerializer(ModelSerializer):
    amount = IntegerField(default=0)

    class Meta(BaseMeta):
        model = EmotionType
        fields = ['id', 'name', 'image', 'description', 'amount']
        extra_kwargs = {
            'amount': {"read_only": True},
            'active': {"write_only": True}
        }


class EmotionCommentSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = EmotionComment


class EmotionPostSerializer(ModelSerializer):
    author = UserViewModelSerializer()

    class Meta(BaseMeta):
        model = EmotionPost
        extra_kwargs = {
            'post': {"write_only": True},
            'active': {"write_only": True}
        }


# end Emotion

class HistoryAuctionSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = HistoryAuction


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
