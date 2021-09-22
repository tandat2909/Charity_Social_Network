import datetime
import decimal

import pytz
import rest_framework
from django.db.models import Count
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from ..models import Notification, Comment, NewsPost, EmotionType, \
    EmotionPost, AuctionItem, HistoryAuction
from ..serializers import EmotionStatisticalSerializer, EmotionPostSerializer, HistoryAuctionCreateSerializer, \
    HistoryAuctionSerializer


class BaseViewAPI:
    list_action_upload_file = []

    def is_view_user_login(self, request, pk):
        """
               return True when request pk is user login current and else
         """
        return bool(str(request.user.id) == pk)

    def is_instance_of_user(self, request, instance=None):
        instance = instance or self.get_object()
        try:
            return bool(request.user.is_authenticated and request.user.id == instance.user.id)
        except:
            return False

    def add_notification(self, title, message, user=None, *args, **kwargs):
        """
            user là instance User được thêm thông báo mặc dịnh sẽ lấy trong request.user
            request: mặc định sẽ lấy self.request của lớp ViewSet
            title: tiêu đề thông báo
            message: nội dung thông báo
            Nếu user và request không lấy được đồng nghĩa với việc không thêm được thông báo và hàm trả về False
            Nếu add thành công sẽ trả về True

        :param title:
        :param message:
        :param user:
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            user = user or self.request.user
            n = Notification(title=title, message=message)
            n.save()
            user.notifications.add(n)
            return True
        except Exception as ex:
            print("add_notification:none user ", ex)
            return False

    def delete_custom(self, request=None, instance=None, *args, **kwargs):
        instance = instance or self.get_object()
        instance.active = False
        instance.save()
        # add thong báo
        if isinstance(instance, NewsPost):
            self.add_notification(title="Xóa bài viết", message='Bạn vừa xóa bài viết "' + instance.title + '"')

        if isinstance(instance, Comment):
            self.add_notification(title="Xóa commment bài viết",
                                  message='Bạn vừa xóa comment "' + instance.content + '"')

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_parsers(self):
        """
            Mặc định dùng JSONParser class
            Nếu action hiện tại có trong list_action_upload_file thì chuyển đổi parser mặc định sang MultiPartParser class
        :return: List instance class Parser
        """
        try:
            if self.action in self.list_action_upload_file:
                return [MultiPartParser(), ]
            return super().get_parsers()
        except:
            return super().get_parsers()

    def is_between_time(self, start, end, intime=datetime.datetime.now(pytz.utc)):
        # print(start, end, intime)

        if start <= intime <= end:
            return True
        elif start > end:
            end_day = datetime.time(hour=23, minute=59, second=59, microsecond=999999)
            if start <= intime <= end_day:
                return True
            elif intime <= end:
                return True
        return False

    def offer(self, request, post=None, instance_auction_item=None):
        offer = request.data.get("offer", None)
        if offer is None:
            raise rest_framework.exceptions.NotFound({"offer": "field is not empty"})
        if post is None and instance_auction_item is None:
            raise rest_framework.exceptions.NotFound()

        try:
            # Nếu bài viết đc truyền vô thì query dữ liệu lấy auction item
            if post is not None and instance_auction_item is None:
                instance_auction_item = AuctionItem.objects.get(post=post.id)
            else:
                # print(instance_auction_item.post)
                post = instance_auction_item.post
            # print(instance_auction_item.start_datetime, instance_auction_item.end_datetime)

            if instance_auction_item.start_datetime.timestamp() > datetime.datetime.now().timestamp():
                raise rest_framework.exceptions.ValidationError({"error": "Phiên đấu giá chưa bắt đầu"})
            if not self.is_between_time(instance_auction_item.start_datetime, instance_auction_item.end_datetime):
                raise rest_framework.exceptions.ValidationError({"error": "Phiên đấu giá đã kết thúc"})
            try:
                if decimal.Decimal(offer) <= instance_auction_item.price_start:
                    raise rest_framework.exceptions.ValidationError(
                        {"offer": "offer không hợp lệ giá phải lớn hơn hoặc bằng giá khởi điểm"})
            except decimal.InvalidOperation:
                raise rest_framework.exceptions.ValidationError(
                    {"offer": "Yêu cầu một số lớn hơn 0, Không phải chuỗi"})

            history_data = {
                "user": request.user,
                "post": post
            }

            try:
                instance = HistoryAuction.objects.get(**history_data)
                instance.price = offer
                instance.save()
                message = 'Bạn vừa cập nhật giá {price} VNĐ cho bài viết {post_title}'.format(
                    price=str(offer),
                    post_title=post.title)

                self.add_notification(title="Thông báo có giá mới", user=post.user, message=message)
                request.user.email_user(subject="[Charity Social Network][Thông báo đấu giá]", message=message)
                return Response({'success': "Cập nhật giá thành công", **HistoryAuctionSerializer(instance).data},
                                status=status.HTTP_200_OK)
            except HistoryAuction.DoesNotExist:
                instance = HistoryAuction.objects.create(**history_data, price=offer)
                self.add_notification(title="Thông báo có giá mới", user=post.user,
                                      message='{username} đề nghị giá {price} VNĐ cho bài viết {post_title}'.format(
                                          username=request.user.get_full_name(),
                                          price=str(offer),
                                          post_title=post.title))
                request.user.email_user(subject="[Charity Social Network][Thông báo đấu giá]",
                                        message="Bạn đã đấu giá sản phẩm")
                return Response(HistoryAuctionSerializer(instance).data, status=status.HTTP_201_CREATED)

        except AuctionItem.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Bài viết không phải loại bài viết đấu giá")


class EmotionViewBase:

    def statistical_emotion_post(self, post_id, **kwargs):
        """
        Thống kê tất cả biểu cảm bài viết
        tất cả các fields của EmotionType và thêm một fields amount
        amount: tổng số lượng mỗi loại biểu cảm mà bài viết có
        các loại biểu cảm không có sẽ không được thêm vào
        :param post_id:
        :return:
        """
        data = EmotionType.objects \
            .filter(emotionpost__post=post_id, emotionpost__active=True) \
            .annotate(amount=Count('id'))
        return data

    def detail_emotions_post(self, post, **kwargs):
        """
        Lấy tất cả emotions post của bài viết theo id bài viết

        :param post_id: id bài viết
        :return: QuerySet<[<EmotionPost: Like>, <EmotionPost: Sad>]>
        """

        instances = post or self.get_object()
        return instances.emotionpost_set.filter(active=True)

    def get_serializer_statistical_emotion_post(self, post_id, **kwargs):
        request = kwargs.get("request", None)
        return EmotionStatisticalSerializer(self.statistical_emotion_post(post_id), many=True, context={
            'request': request or self.request
        })

    def get_serializer_detail_emotions_post(self, post=None, **kwargs):
        """
        Trả về đối tượng EmotionPostSerializer
        :param post_id:
        :param kwargs:
        :return:
        """

        return EmotionPostSerializer(self.detail_emotions_post(post, **kwargs), many=True,
                                     context={"request": self.request})

    def create_or_update_emotion(self, data, models, **kwargs):
        '''
            lấy emotion type id ra kiểm tra nó có tồn tại không
            - lấy thông tin emotion post ra nếu có thì cập nhật lại cái type mới nếu không có tạo mới
        :param data:
        :param kwargs:
        :return:
        '''
        emotion_type = data.pop("type_id")
        assert EmotionType.objects.get(id=emotion_type)

        try:
            instance = models.objects.get(**data)
            instance.type_id = emotion_type
            instance.save()
        except models.DoesNotExist:
            instance = models.objects.create(**data, type_id=emotion_type)

        return instance
