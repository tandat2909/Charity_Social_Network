from rest_framework.serializers import *
from django.contrib.auth.models import Group, Permission
from .models import *
from .validators import PasswordValidator


class BaseMeta:
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


# class UserViewUserOtherSerializer(ModelSerializer):
#     # groups = GroupsSerializer(many=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'gender']


class UserViewModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'first_name', 'last_name']


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


# Post
class CategoryPostSerializer(ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "name"]


class HashtagsSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'description']


class PostSerializer(ModelSerializer):
    user = UserViewModelSerializer()
    category = CategoryPostSerializer()
    hashtag = HashtagsSerializer(many=True)

    class Meta(BaseMeta):
        model = NewsPost
        extra_kwargs = {
            'active': {'write_only': True},
            'is_show': {'write_only': True},
            'id': {'read_only': True},
        }


class AuctionItemSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = AuctionItem
        fields = ["id", "post", "price_start"]
        extra_kwargs = {
            "id": {"read_only": True}
        }


class PostCreateSerializer(ModelSerializer):
    price_start = DecimalField(required=False, max_digits=50, decimal_places=2)

    # user_id = HiddenField(default=None)

    class Meta:
        model = NewsPost
        fields = ["id", "category", "hashtag", "description", "content", "title", 'price_start', "user",'image']
        read_only_fields = ["user", ]
        extra_kwargs = {
            'id': {'read_only': True},

        }

    def create(self, validated_data, **kwargs):
        print(validated_data)
        data_auction = {"price_start": validated_data.pop("price_start", None)}
        print(data_auction)
        if data_auction.get("price_start"):
            instance_news_post = super().create(validated_data)
            data_auction["post"] = instance_news_post.id
            try:
                serializer_auction = AuctionItemSerializer(data=data_auction)
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


class EmotionTypeSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = EmotionType
        fields = ["id", "name"]


class EmotionCommentSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = EmotionComment


class EmotionPostSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = EmotionPost


class HistoryAuctionSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = HistoryAuction


class OptionReportSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = OptionReport
        filter = None


class ReportSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = Report


class AuctionItemSerializer(ModelSerializer):
    class Meta(BaseMeta):
        model = AuctionItem
