import datetime

import pytz
from django.db.models import Count
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from ..models import Notification, Comment, NewsPost, EmotionType, \
    EmotionPost
from ..serializers import EmotionStatisticalSerializer, EmotionPostSerializer


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

    def add_notification(self, title, message, user=None, request=None, *args, **kwargs):
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
            user = user or request.user or self.request.user
            n = Notification(title=title, message=message)
            n.save()
            user.notifications.add(n)
            return True
        except Exception as ex:
            print(ex)
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
        data = EmotionType.objects.all() \
            .filter(emotionpost__post=post_id, emotionpost__active=True) \
            .annotate(amount=Count('id'))
        return data

    def detail_emotions_post(self, post_id, **kwargs):
        """
        Lấy tất cả emotions post của bài viết theo id bài viết

        :param post_id: id bài viết
        :return: QuerySet<[<EmotionPost: Like>, <EmotionPost: Sad>]>
        """

        instances = EmotionPost.objects.filter(active=True, post=post_id)
        return instances

    def get_serializer_statistical_emotion_post(self, post_id, **kwargs):
        request = kwargs.get("request", None)
        return EmotionStatisticalSerializer(self.statistical_emotion_post(post_id), many=True, context={
            'request': request or self.request
        })

    def get_serializer_detail_emotions_post(self, post_id, **kwargs):
        """
        Trả về đối tượng EmotionPostSerializer
        :param post_id:
        :param kwargs:
        :return:
        """

        return EmotionPostSerializer(self.detail_emotions_post(post_id, **kwargs), many=True,
                                     context={"request": self.request})

    def create_or_update_emotion(self, data, models, **kwargs):
        '''
            lấy emotion type id ra kiểm tra nó có tồn tại không
            - lấy thông tin emotion post ra nếu có thì cập nhật lại cái type mới nếu không có tạo mới
        :param data:
        :param kwargs:
        :return:
        '''
        emotion_type = data.pop("emotion_type_id")
        assert EmotionType.objects.get(id=emotion_type)
        instance = None
        try:
            instance = models.objects.get(**data)
            instance.emotion_type_id = emotion_type
            instance.save()
        except models.DoesNotExist:
            instance = models.objects.create(**data, emotion_type_id=emotion_type)
            self.get_object().emotions.add(instance)

        return instance
