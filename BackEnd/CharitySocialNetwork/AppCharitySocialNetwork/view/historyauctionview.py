import decimal

import rest_framework
from rest_framework import permissions
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models import HistoryAuction


from ..serializers import HistoryAuctionSerializer
from ..view.baseview import BaseViewAPI


class HistoryAuctionViewSet(UpdateModelMixin, DestroyModelMixin, BaseViewAPI, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = HistoryAuction.objects.filter(active=True)
    serializer_class = HistoryAuctionSerializer

    def update(self, request, *args, **kwargs):
        if super().is_instance_of_user(request, self.get_object()):
            if request.data.get("user", None):
                raise rest_framework.exceptions.ValidationError(
                    {"error": "Không thể thay đổi user chỉ được thay đổi mệnh giá tiền và mô tả"})
            price_start = self.get_object().post.info_auction.first().price_start
            if price_start.__gt__(decimal.Decimal(request.data.get("price"))):
                raise rest_framework.exceptions.ValidationError({"price": "Giá không thể thấp hơn giá ban đầu"})
            return super().update(request, *args, **kwargs)
        raise rest_framework.exceptions.PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        if super().is_instance_of_user(request, self.get_object()):
            return super().destroy(request, *args, **kwargs)
        raise rest_framework.exceptions.PermissionDenied()
