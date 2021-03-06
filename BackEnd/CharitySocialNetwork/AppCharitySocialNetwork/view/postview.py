import datetime
import decimal
import re
from collections import OrderedDict

import cloudinary
import rest_framework
from MySQLdb import IntegrityError
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, OR
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from ..filters import DjangoFilterBackendCustom
from ..models import NewsPost, AuctionItem, HistoryAuction, Comment, \
    EmotionPost, EmotionType, NewsCategory, User, Hashtag
from ..paginators import PostPagePagination, CommentPagePagination, ImagePagePagination
from ..permission import PermissionUserMod
from ..serializers import PostListSerializer, EmotionPostSerializer, \
    PostCreateSerializer, PostChangeFieldIsShow, CommentSerializer, CommentCreateSerializer, ReportPostCreateSerializer, \
    PostSerializer, PostDetailSerializer, ReportPostSerializer, AuctionItemSerializer, HistoryAuctionCreateSerializer, \
    CategoryPostSerializer, HashtagsSerializer, UserViewModelSerializer, HistoryAuctionSerializer, \
    AuctionItemViewSerializer, PostImageSerializer
from ..view.baseview import BaseViewAPI, EmotionViewBase


class PostViewSet(BaseViewAPI, EmotionViewBase, ModelViewSet):
    queryset = NewsPost.objects.filter(active=True)
    # serializer_class = PostSerializer
    # lookup_field = {'pk', 'user_id', "user_name", "title"}
    # lookup_url_kwarg = "user"
    list_action_upload_file = ["create", 'update', 'partial_update', 'create_report']
    # pagination_class = PostPagePagination
    filter_backends = [DjangoFilterBackendCustom, OrderingFilter, SearchFilter]
    filterset_fields = [
        'category',
        'hashtag',
        'user',
        'created_date'
    ]
    ordering_fields = [
        "id",
        "user",
        "category",
        "hashtag",
        "description",
        "created_date",
        "title"
    ]
    search_fields = [
        # t??m ki???m theo th??? t??? t??? tr??n xu???ng
        'title',
        'description',
        'hashtag__name',
        'content',
        'category__name',
    ]

    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action in ["create_comment", "get_comment", "list"]:
            return self.queryset.filter(is_show=True)
        return self.queryset

    def get_permissions(self):
        if self.action in ['list', 'get_comments', 'get_emotion_post','ckeditor_upload', 'retrieve', 'category',
                           "get_all_image_post_user"]:
            return [permissions.AllowAny(), ]
        if self.action in ["is_post_allowed", "get_list_pending_post"]:
            return [OR(PermissionUserMod(), IsAdminUser()), ]
        return [permissions.IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.action in ["retrieve", ]:
            return PostDetailSerializer
        if self.action in ['list', 'get_post_by_user']:
            return PostListSerializer
        if self.action in ['category']:
            return CategoryPostSerializer
        if self.action in ['create_or_update_or_delete_emotion_post', ]:
            return EmotionPostSerializer
        if self.action in ["create", 'update', 'partial_update']:
            return PostCreateSerializer
        if self.action.__eq__("is_post_allowed"):
            return PostChangeFieldIsShow
        if self.action in ['get_comments', ]:
            return CommentSerializer
        if self.action in ['create_comment', ]:
            return CommentCreateSerializer
        if self.action in ["create_report", ]:
            return ReportPostCreateSerializer
        if self.action in ['set_auctioneer_winning', 'offer_item']:
            return None

        return PostSerializer

    def retrieve(self, request, *args, **kwargs):

        if self.is_instance_of_user(request, self.get_object()) or request.user.is_superuser:
            return Response(self.get_serializer(self.get_object(), context={"request": request}).data,
                            status=status.HTTP_200_OK)
        if not self.get_object().is_show:
            raise rest_framework.exceptions.NotFound()
        data = self.get_serializer(self.get_object()).data.copy()
        data["historyauction"] = []
        try:
            if request.user.is_authenticated and AuctionItem.objects.filter(post=self.get_object().id).exists():
                instance_history_auction_of_user_current = HistoryAuction.objects.get(user=request.user.id,
                                                                                      post=self.get_object().id,
                                                                                      active=True)
                data["historyauction"] = [HistoryAuctionSerializer(instance_history_auction_of_user_current).data, ]
        except HistoryAuction.DoesNotExist:
            print("user kh??ng ?????u gi??")
        finally:
            return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        <pre>
            M???c ?????nh l???y 30 b??i vi???t m???i nh???t v?? ???????c mod duy???t cho t???t c??? ng?????i d??ng
            <b>Filter:</b>
                L???c d??? li???u ???????c ch??? ?????nh
               <b>Params: </b>
                    + user = <id:int>: l???y t???t c??? b??i vi???t c???a user theo id ???????c duy???t
                    + category = <category_id:id>: tr??? v??? list b??i vi???t theo danh m???c (lo???i b??i vi???t)
                    + hashtag = <n???i dung>: tr??? v??? list b??i vi???t c?? n???i dung hashtag c???n t??m
                    + created_date: tr??? v??? list b??i vi???t t??? ng??y <data_from> ?????n <date_to>
                V?? d???: v?? d???: http://localhost:8000/api/newspost/?category=1&hashtag=1&hashtag=2
                    => tr??? ra k???t qu??? c??c b??i vi???t thu???c danh m???c c?? id l?? 1 v?? c??c b??i vi???t c?? hashtag id 1 ho???c 2
               <b>L??u ??:</b>
                    C??c fields <b>user,category,hashtag</b> l?? id y??u c???u <b>ki???u d??? li???u</b> l?? <b>s??? nguy??n</b>
            <b>Ordering:</b>
                Ch??? ?????nh c??c tr?????ng s???p x???p theo th??? t??? t??ng d???n ho???c gi???n d???n
                C??c tham s??? ch??? ?????nh s???p x???p
                <b>Params:</b>
                    + <b>id:</b> s???p x???p theo id b??i vi???t
                    + <b>user:</b> s???p x???p theo id user
                    + <b>category:</b> s???p x???p theo category_id
                    + <b>hashtag:</b> s???p x???p theo hashtag_id
                    + <b>description:</b> s???p x???p theo ch??? c??i ?????u description
                    + <b>created_date:</b> s???p x???p theo ng??y t???o b??i vi???t
                    + <b>title:</b> s???p x???p theo ch??? c??i ?????u c???a ti??u ?????
                V?? d???: http://localhost:8000/api/newspost/?ordering=id
                    => tr??? v??? k???t qu??? ???????c s???p x???p theo id b??i vi???t t??ng d???n
                <b>L??u ??:</b>
                    ????? ch???n ch??? ????? s???p x???p gi???m d???n ta th??m d???u '-' tr?????c t??n field ???????c ch??? ?????nh
                       + v?? d???: http://localhost:8000/api/newspost/?ordering=-category
                       => url tr??n tr??? k???t qu??? s???p x???p gi???m d???n theo category_id
            <b>Search:</b>
                T??m ki???m t???t c??? b??i vi???t c?? n???i dung li??n quan tr??n c??c tr?????ng ???????c c???u h??nh s???n
                <b>Fields:</b> ['title','description','hashtag__name','content','category__name']
                <b>Param:</b>
                    + <b>search</b>: g??n n???i dung c???n t??m ki???m
                V?? d???: http://localhost:8000/api/newspost/?search=tr???+em
                    tr??? v??? t???t c??? b??i vi???t c?? n???i dung li??n quan
        </pre>
        """
        # print(request.query_params)
        queryset = self.get_queryset()
        # print(queryset.query)
        self.pagination_class = PostPagePagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # x??a b??i vi???t c???a ch??nh user ???? n???u kh??c th?? kh??ng ??c
        instance = self.get_object()
        if instance.user_id == request.user.id:
            return self.delete_custom(request, *args, **kwargs)
        raise PermissionDenied()

    def create(self, request, *args, **kwargs):
        '''
            price_start: t???o b??i vi???t ?????u gi??
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        # print(request.data,type(request.data.getlist("hashtag",None)))
        try:
            hashtag = request.data.getlist("hashtag", None)
        except:
            hashtag = request.data.get("hashtag", None)

        instance = serializer.save(**{"user": request.user, 'hashtag': hashtag})
        self.add_notification(**settings.NOTIFICATION_MESSAGE.get("add_post"))

        return Response(PostSerializer(instance, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if self.is_instance_of_user(request, self.get_object()):
            return super().update(request, *args, **kwargs)
        raise PermissionDenied()

    def perform_update(self, serializer, **kwargs):
        try:
            hashtag = self.request.data.getlist("hashtag", None)
        except:
            hashtag = self.request.data.get("hashtag", None)
        kwargs["hashtag"] = hashtag
        kwargs["is_show"] = False
        # print("update view: hashtag: ", hashtag)
        serializer.save(**kwargs)
        self.add_notification(**settings.NOTIFICATION_MESSAGE.get("update_post"))

    @action(methods=["PATCH"], detail=True, url_path="is-post-allowed")
    def is_post_allowed(self, request, pk, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        if instance.is_show and serializer.data["is_show"]:
            return Response({"error": "B??i vi???t ???? ???????c duy???t"}, status=status.HTTP_400_BAD_REQUEST)
        instance.is_show = serializer.data["is_show"]
        instance.save()
        if instance.is_show:
            self.add_notification(title="Duy???t b??i",
                                  user=instance.user,
                                  message="B??i vi???t {post_title} ???? ???????c duy???t".format(post_title=instance.title)
                                  )
            if instance.category.id == 1:
                # print(Group.objects.get(name="User").user_set.all())
                for u in Group.objects.get(name="User").user_set.all():
                    # print(instance.info_auction.first(), u)
                    if u.id != instance.user.id:
                        self.add_notification(title="S??? ki???n ?????u gi??", user=u,
                                              message="{title} di???n ra v??o ng??y {start} - {end}".
                                              format(
                                                  title=instance.title,
                                                  start=instance.info_auction.first().start_datetime,
                                                  end=instance.info_auction.first().end_datetime
                                              ))
        return Response(status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="user")
    def get_post_by_user(self, request, *args, **kwargs):
        '''
            Tr??? v??? t???t c??? b??i vi???t c???a user ??ang ????ng nh???p bao g???m c??c b??i ch??a duy???t c???a user
            C???n ????ng nh???p t??i kho???n user
            filter:
                + c?? t???t c??? c??c tham s??? filter list post
                + th??m filter b??i vi???t ch??a duy???t ho???c ???? duy???t b??i c???a user ??ang ????ng nh???p
                    - browser = 1 : filter l???y t???t c??? b??i vi???t ???????c duy???t
                    - browser = 0 : filter l???y t???t c??? b??i vi???t ch??a duy???t

        '''
        browser = request.query_params.get("browser", None)
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user.id))
        if browser:
            try:
                queryset = queryset.filter(is_show=bool(int(browser)))
            except:
                pass
        self.pagination_class = PostPagePagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="list_pending_post")
    def get_list_pending_post(self, request):
        """
            C???n ????ng nh???p t??i kho???n user mod (t??i kho???n duy???t b??i)

        """
        queryset = self.filter_queryset(self.get_queryset().filter(is_show=False))
        self.pagination_class = PostPagePagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # comment

    @action(methods=["GET"], detail=True, url_path="comments")
    def get_comments(self, request, pk, **kwargs):
        '''
            m???c ?????nh l???y 30 comment ?????u ti??n
        '''
        try:
            # comment_parent = request.query_params.get("comment", None)
            # l???y t???t c??? comment kh??ng c?? comment_parent
            queryset = self.get_object().comment_set.filter(active=True, comment_parent=None)
            self.pagination_class = CommentPagePagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=True, url_path="comment")
    def create_comment(self, request, pk, **kwargs):
        """
            t???o comment b??i vi???t
            <b>Param</b>
                c?? 2 tham s???:
                + content: n???i dung content
                + comment_parent: <comment_id>
                l??u ??: N???u kh??ng ????? tham s??? comment_parent m???c ?????nh t???o comment cho b??i vi???t ng?????c l???i n???u c?? s??? t???o comment con cho comment
            <b>Require</b>
                + Y??u c???u ????ng nh???p
                + content
            API v2:
                thay ?????i url
        """

        serializer_comment = CommentCreateSerializer(data={**request.data})
        serializer_comment.is_valid(raise_exception=True)
        instance_comment = serializer_comment.save(**{"user": request.user, "post": self.get_object()})
        try:
            if request.data.get("comment_parent", None) is not None:
                # print(self.get_object().user)
                # th??ng b??o ch??? ch??? comment parent c?? comment m???i
                self.add_notification(title="B??nh lu???n m???i",
                                      user=instance_comment.comment_parent.user,
                                      message=request.user.get_full_name() +
                                              " ???? ph???n h???i b??nh lu???n c???a b???n v??? b??i vi???t c???a " +
                                              self.get_object().user.get_full_name())

            # ki???m tra b??i vi???t hi???n t???i c?? ph???i c???a user ??ang b??nh lu???n n???u ph???i s??? kh??ng add th??ng b??o
            if not self.is_instance_of_user(request, self.get_object()):
                self.add_notification(title="B??nh lu???n m???i",
                                      message=request.user.get_full_name() + " ???? b??nh lu???n b??i vi???t c???a b???n",
                                      user=self.get_object().user)
            return Response(data=CommentSerializer(instance_comment).data, status=status.HTTP_201_CREATED)
        except Comment.DoesNotExist:
            raise rest_framework.exceptions.NotFound({"detail": "comment_parent not exist"})

    # end comment

    # emotion

    @action(methods=["GET"], detail=True, )
    def get_emotion_post(self, request, pk, **kwargs):
        post_id = self.get_object().id
        serializer_statistical = self.get_serializer_statistical_emotion_post(post_id)
        serializer_emotion_post = self.get_serializer_detail_emotions_post()
        return Response(data={
            'statistical': serializer_statistical.data,
            'data': serializer_emotion_post.data
        }, status=status.HTTP_200_OK)

    @action(methods=["PATCH"], detail=True, url_path='emotions', name="emotions")
    def create_or_update_or_delete_emotion_post(self, request, pk, **kwargs):
        """
        <pre>
            <b>Ch???c n??ng:</b>
                + add: Th??m bi???u c???m cho b??i vi???t
                + update: Thay ?????i lo???i bi???u c???m
                + delete: X??a bi???u c???m c???a user v???i b??i vi???t
            <b>Param:</b>
                + emotion_type: <id> ch??? ?????nh lo???i bi???u c???m, Ki???u d??? li???u <b>s??? nguy??n</b>
                + action: [delete,] ch??? ?????nh tham s??? n??y ????? th???c hi???n <b>delete</b> bi???u c???m
            <b>V?? d???:</b>
                + action add: http://localhost:8000/api/newspost/6/emotions/?emotion_type=3
                => th??m ho???c update bi???u c???m m???i
                + action delete:http://localhost:8000/api/newspost/6/emotions/?action=delete
                => delete bi???u c???m user d??nh cho b??i vi???t
                    response: status code 204
        </pre>
        """
        if request.query_params.get("action", '').__eq__('delete'):
            EmotionPost.objects.get(user_id=request.user.id, post_id=self.get_object().id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = {
            'user_id': request.user.id or None,
            'post_id': self.get_object().id or None,
            'type_id': request.query_params.get("emotion_type", None),
        }
        try:

            instance_emotion = self.create_or_update_emotion(data, EmotionPost)
            self.add_notification(title="",
                                  message=(self.request.user.get_full_name() or self.request.user.username) +
                                          " " + instance_emotion.type.name + ' b??i vi???t " ' + self.get_object().title + ' " c???a b???n"',
                                  user=self.get_object().user
                                  )
            return Response(data=EmotionPostSerializer(instance_emotion, context={"request": request}).data,
                            status=status.HTTP_200_OK)
        except EmotionType.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Emotion type not exist")

    # end emtion

    # Report
    @action(methods=["POST", ], detail=True, url_path="report")
    def create_report(self, request, pk, **kwargs):
        """
            + Ch???c n??ng:
                - T???o report b??i vi???t
            + Method: POST
            + Authorization: True
            + Request Body:

        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(**{"post": self.get_object(), "user": request.user})
        # todo l???y user ra th??ng b??o cho t???t c??? admin kh??ng ???????c performance
        instance_user_admin = User.objects.filter((
                                                          Q(is_superuser=True) |
                                                          Q(is_staff=True) |
                                                          Q(user_permissions__codename__contains='mod')
                                                  )
                                                  & Q(is_active=True))
        message = 'Ng?????i d??ng {name} ???? report \n{content}'.format(name=self.request.user.get_full_name(),
                                                                   content=instance.__str__())
        for user in instance_user_admin:
            self.add_notification(title='Report', message="B??i vi???t " + self.get_object().title, user=user)
            user.email_user(subject="[Charity Social Network][Report][News Post]", message=message)

        request.user.email_user(subject="[Charity Social Network][Report]",
                                message=instance.__str__()
                                        + "\n C???m ??n b???n ???? Report ch??ng t??i s??? xem x??t "
                                          "v?? g???i th??ng b??o cho b???n s???m nh???t")
        return Response(ReportPostSerializer(instance,context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

    @action(methods=["PATCH"], detail=True)
    def set_auctioneer_winning(self, request, pk, **kwargs):
        """
        <pre>
            Ch???n ng?????i ?????u gi?? chi???n th???ng cho phi??n ?????u gi??
            <b>request params:</b>
                +id: post_id:int id b??i vi???t
            <b>Body:</b>
                + history_auction: history_auction_id:int id l???ch s??? ng?????i ?????u gi??
        </pre>
        """
        # ki???m tra c?? ph???i b??i vi???t c???a user kh??ng
        if not self.is_instance_of_user(request, self.get_object()):
            raise PermissionDenied()
        try:
            # ki???m tra request c?? g???i phi???u ?????u gi?? l??n kh??ng
            history_auction_id = request.data.get("history_auction", None)
            if history_auction_id is None or type(history_auction_id) is not int:
                raise rest_framework.exceptions.ValidationError(
                    "Require history_auction_id not none and Require history_auction_id is Integer")
            # l???y phi???u ?????u gi?? ?????ng th???i ki???m tra n?? t???n t???i kh??ng
            instance_history_auction = HistoryAuction.objects.get(pk=history_auction_id)
            # l???y phi??n ?????u gi?? ????ng th???i ki???m tra n?? c?? ph???i b??i vi???t ?????u gi?? kh??ng
            instance_auction_item = AuctionItem.objects.get(post=self.get_object().id)
            # pass 2 ??i???u ki???n tr??n g??n ng?????i chi???n th???ng v?? gi?? ng?????i chi???n th???ng ????a ra
            instance_auction_item.receiver = instance_history_auction.user
            instance_auction_item.price_received = instance_history_auction.price

            instance_auction_item.save()

            self.add_notification(title="Th??ng b??o ?????u gi??",
                                  message="Ch??c m???ng b???n l?? ng?????i chi???n th???ng trong bu???i ?????u gi?? " + self.get_object().title,
                                  user=instance_history_auction.user
                                  )
            self.add_notification(title="Th??ng b??o th??nh to??n ?????u gi??",
                                  message=str(instance_auction_item.price_received) +
                                          'VN?? l?? s??? ti???n b???n ph???i thanh to??n cho ban t??? ch???c t??? thi???n c???a b??i vi???t "' +
                                          self.get_object().title,
                                  user=instance_history_auction.user
                                  )
            instance_history_auction.user.email_user(subject="[Charity Social Network][Th??ng b??o ?????u gi??]",
                                                     message="Ch??c m???ng b???n l?? ng?????i chi???n th???ng ?????u gi??"
                                                     )

            return Response(AuctionItemViewSerializer(instance_auction_item).data, status=status.HTTP_200_OK)
        except AuctionItem.DoesNotExist:
            raise rest_framework.exceptions.NotFound("B??i vi???t kh??ng ph???i lo???i b??i vi???t ?????u gi??")
        except HistoryAuction.DoesNotExist:
            raise rest_framework.exceptions.NotFound("L???ch s??? ?????u gi?? n??y kh??ng t???n t???i")
        except NewsPost.DoesNotExist:
            raise rest_framework.exceptions.NotFound("B??i vi???t kh??ng t???n t???i")

    def is_show(self):
        """
            Ki???m tra b??i vi???t s???n s??ng hi???n th??? cho ng?????i d??ng xem hay ch??a
            n???u b??i vi???t s??n s??ng return True ng?????c return throw exception, k??m m?? l???i status code 404 cho client
        :return: True
        :exception rest_framework.exceptions.NotFound
        """
        if not self.get_object().is_show:
            raise rest_framework.exceptions.NotFound({"error": "B??i vi???t ??ang ch??? ???????c duy???t"})
        return True

    @action(methods=["PATCH"], detail=True, url_path="offer")
    def offer_item(self, request, pk, **kwargs):
        self.is_show()
        return self.offer(request, post=self.get_object())

    @action(methods=["DELETE"], url_path="hashtag/(?P<hash_tag_id>[a-z0-9]+)/delete", detail=True)
    def delete_hashtag(self, request, pk, hash_tag_id, **kwargs):
        try:
            if self.is_instance_of_user(request, self.get_object()):
                # print(hash_tag_id, pk, kwargs)
                instance_post = self.get_object()
                instance_post.hashtag.get(pk=hash_tag_id).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            raise rest_framework.exceptions.PermissionDenied()
        except ValueError as ex:
            return Response({"error": ex.__str__()}, status=status.HTTP_400_BAD_REQUEST)
        except Hashtag.DoesNotExist:
            return Response({"error": "B??i vi???t kh??ng c?? hash tag n??y"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["GET"], detail=False, url_path="category", )
    def category(self, request):
        instances = NewsCategory.objects.filter(active=True)
        serializer = CategoryPostSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="ckeditor/upload")
    def ckeditor_upload(self, request, **kwargs):
        try:
            uploaded_file = request.FILES["upload"]
            file = cloudinary.uploader.upload(uploaded_file)
            # print("sssssss",file.get("secure_url",None))
            filename = file.get("public_id")
            url = file.get("secure_url")
            retdata = {"url": url, "uploaded": "1", "fileName": filename}
            return Response(retdata, status=status.HTTP_200_OK)
        except:
            return Response({'error': "L???i upload file"}, status=400)

    @action(methods=["GET"], detail=False, url_path="get-all-image-post-user/(?P<user_id>[0-9]+)")
    def get_all_image_post_user(self, request, user_id, **kwargs):
        """
            L???y t???t c??? h??nh ???nh theo ng?????i d??ng m?? b??i vi???t ???? ???????c duy???t

        """
        query_set = self.get_queryset().filter(user=user_id, is_show=True, image__isnull=False).order_by(
            "-created_date")
        # print(query_set.query)
        self.pagination_class = ImagePagePagination
        return self.get_paginated_response(PostImageSerializer(self.paginate_queryset(query_set), many=True).data, )
