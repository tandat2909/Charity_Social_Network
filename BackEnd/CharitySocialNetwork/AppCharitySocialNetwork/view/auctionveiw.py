from rest_framework import permissions
from rest_framework.decorators import action

from ..models import AuctionItem
from ..serializers import AuctionItemSerializer, AuctionItemViewSerializer
from ..view.baseview import BaseViewAPI
from rest_framework.viewsets import *
from rest_framework.generics import *


class AuctionViewSet(BaseViewAPI, GenericViewSet, RetrieveAPIView):
    queryset = AuctionItem.objects.filter(active=True)
    serializer_class = AuctionItemViewSerializer

    def get_permissions(self):
        if self.action in ["offer", ]:
            return [permissions.IsAuthenticated(), ]
        return [permissions.AllowAny()]

    @action(methods=["PATCH"], url_path="offer", detail=True)
    def offer_item(self, request, pk, **kwargs):
        '''
            + Chức năng: ra giá cho một sản phẩm đang trong quá trình đấu giá
                Nếu thông tin đấu giá đã có rồi thì sẽ cập nhật giá hiện tại
            + Request body:
                - offer: đưa ra giá mong muốn, yêu cầu giá phải lớn hơn giá khởi điểm. Kiểu dữ liệu <b>decimal</b>
            + Response body:
                - Thông tin lịch sử đấu giá
        '''
        return self.offer(request, instance_auction_item=self.get_object())

