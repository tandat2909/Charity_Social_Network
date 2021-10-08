import rest_framework.exceptions
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import AuctionItem
from ..serializers import AuctionItemSerializer, AuctionItemViewSerializer, OrderViewSerializer
from ..view.baseview import BaseViewAPI
from rest_framework.viewsets import *
from rest_framework.generics import *


class AuctionViewSet(BaseViewAPI, GenericViewSet, RetrieveAPIView):
    queryset = AuctionItem.objects.filter(active=True)
    serializer_class = AuctionItemViewSerializer

    def get_permissions(self):
        if self.action in ["retrieve", ]:
            return [permissions.AllowAny(), ]
        return [permissions.IsAuthenticated(), ]

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

    @action(methods=["GET"], detail=True, url_path="confirm_sent")
    def confirm_sent(self, request, pk, **kwargs):
        instance_auction = self.get_object()
        if self.is_instance_of_user(request, instance_auction.post):
            if not instance_auction.is_paid() or instance_auction.status is AuctionItem.UNPAID:
                return Response({"error": "Hóa đơn chưa được thanh toán, Vui lòng kiểm tra và thanh toán"},
                                status=status.HTTP_400_BAD_REQUEST)
            if instance_auction.status is not AuctionItem.NOT_YET_SHIPPED:
                return Response({"error": "Hóa đơn đã được xác nhận"}, status=status.HTTP_400_BAD_REQUEST)

            # khi chủ bài viết nhấn xác nhận đã gửi hàng
            instance_auction.status = AuctionItem.SHIPPING
            # print(instance_auction.status,AuctionItem.SHIPPING)
            instance_auction.save()
            order_id = instance_auction.transaction.order_id
            self.add_notification("Giao Hàng",
                                  user=instance_auction.receiver,
                                  message='Người sở hữu bài viết "{title}" đã chuyển đơn hàng {order_id}. '
                                          'Vui lòng chờ trong ít ngày sẽ nhận được sản phẩm'.
                                  format(title=instance_auction.post.title, order_id=order_id))
            self.add_notification("Xác nhận vận chuyển",
                                  user=request.user,
                                  message='Xác nhận đã chuyển sản phẩm đấu giá "{title}" thành công.'
                                          '\nVới mã đơn hàng "{order_id}" '
                                  .format(title=instance_auction.post.title,
                                          order_id=order_id)
                                  )

            request.user.email_user(subject="[Charity Social Network][Confirm Shipped]",
                                    message='Bạn vừa xác nhận đã vận chuyển đơn hàng "{order_id}" '.format(
                                        order_id=order_id)
                                    )
            instance_auction.receiver.email_user(subject="[Charity Social Network][Shipping]",
                                                 message='Người sở hữu bài viết "{title}" đã chuyển đơn hàng {order_id}.' \
                                                         'Vui lòng chờ trong ít ngày sẽ nhận được sản phẩm'.
                                                 format(title=instance_auction.post.title, order_id=order_id))
            return Response({"success": "Xác nhận thành công"}, status=status.HTTP_200_OK)

        raise rest_framework.exceptions.PermissionDenied()

    @action(methods=["GET"], detail=True, url_path="confirm_received")
    def confirm_received(self, request, pk, **kwargs):
        instance_auction_item: AuctionItem = self.get_object()
        if request.user.pk == instance_auction_item.receiver.pk:
            if instance_auction_item.status is AuctionItem.NOT_YET_SHIPPED:
                return Response({"error": "Đơn hàng chưa được vận chuyển"}, status.HTTP_400_BAD_REQUEST)
            if instance_auction_item.status is AuctionItem.SHIPPED:
                return Response({"error": "Đơn hàng đã nhận"}, status=status.HTTP_400_BAD_REQUEST)
            instance_auction_item.status = AuctionItem.SHIPPED
            instance_auction_item.save()
            self.add_notification("Xác nhận đơn hàng",
                                  message="Cảm ơn bạn đã xác nhận đơn hàng {order_id} ".
                                  format(order_id=instance_auction_item.transaction.order_id), user=request.user)

            message = "{customer_fullname} đã nhận được đơn hàng {order_id} . " \
                      "Bạn vui lòng liên hệ admin để nhận tiền trong vòng 15 ngày nhé".format(
                customer_fullname=request.user.get_full_name(),
                order_id=instance_auction_item.transaction.order_id)

            self.add_notification("Xác nhận đơn hàng", message=message, user=instance_auction_item.post.user)
            instance_auction_item.post.user.email_user(subject="[Charity Social Network][Shipped]", message=message
                                                       )

            return Response({"success": "Xác nhận thành công"}, status.HTTP_200_OK)

        raise rest_framework.exceptions.PermissionDenied()

    @action(methods=["GET"], detail=False, url_path="order")
    def order(self, request, **kwargs):
        orders_of_user = request.user.auctionitem_set.all()
        return Response(OrderViewSerializer(orders_of_user, many=True).data, status=status.HTTP_200_OK)
