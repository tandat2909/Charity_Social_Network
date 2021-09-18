from rest_framework import permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import Comment, EmotionComment, EmotionType
from ..serializers import CommentSerializer, CommentCreateSerializer, \
    EmotionCommentSerializer
from ..view.baseview import BaseViewAPI
from ..view.emotionview import EmotionViewBase


class CommentViewSet(DestroyModelMixin, RetrieveUpdateAPIView, EmotionViewBase, GenericViewSet, BaseViewAPI):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    # def retrieve(self, request, *args, **kwargs):
    #     post_id = kwargs.get("post_id", None)
    #     serializer_statistical = self.get_serializer_statistical_emotion_post(post_id)
    #     serializer_emotion_post = self.get_serializer_detail_emotions_post(post_id)
    #     return Response(data={
    #         'statistical': serializer_statistical.data,
    #         'data': serializer_emotion_post.data
    #     }, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["retrieve", ]:
            return [permissions.AllowAny(), ]
        return [permissions.IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.action in ["update", 'partial_update']:
            return CommentCreateSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        if self.is_instance_of_user(request, self.get_object()):
            super().update(request, *args, **kwargs)
            return Response(CommentSerializer(self.get_object(), context={"request": request}).data, status.HTTP_200_OK)
        raise permissions.exceptions.PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        if self.is_instance_of_user(request):
            return self.delete_custom(request, self.get_object())
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=["PATCH"], detail=True, url_path="emotions")
    def create_or_update_or_delete_emotion_comment(self, request, pk, **kwargs):
        if request.query_params.get("action", '').__eq__('delete'):
            ins = EmotionComment.objects.get(author_id=request.user.id, comment_id=self.get_object().id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'user_id': request.user.id or None,
            'comment_id': self.get_object().id or None,
            'type_id': request.query_params.get("emotion_type", None),
        }
        try:
            instance_emotion = self.create_or_update_emotion(data, EmotionComment)
            return Response(data=EmotionCommentSerializer(instance_emotion, context={"request": request}).data,
                            status=status.HTTP_200_OK)
        except EmotionType.DoesNotExist:
            raise exceptions.NotFound("Emotion type not exist")
