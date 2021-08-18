from django.db.models import Count
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models import EmotionType, EmotionPost
from ..serializers import EmotionTypeSerializer, \
    EmotionStatisticalSerializer, EmotionPostSerializer


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



class EmotionTypeViewSet(ListModelMixin, GenericViewSet):
    queryset = EmotionType.objects.filter(active=True)
    serializer_class = EmotionTypeSerializer
    pagination_class = None

