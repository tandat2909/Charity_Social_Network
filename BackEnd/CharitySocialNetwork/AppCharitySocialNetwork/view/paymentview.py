"""
    + Tạo hóa đơn => gửi lên momo => lấy link thanh toán => trả về cho client link => link tồn tại trong 7 ngày
    + Tạo link Chờ thông báo từ server momo gửi về
        - quá hạn:
            + thông báo cho chủ sở hữu vật đấu giá quá hạn thanh toán
            + Hủy cho chủ sở hữu
                - cập nhật lại người chiến thắng
                - là mở đấu giá lại
                - hủy lun kết quả
        - thành công:
            + Cập nhật thông tin thanh toán vô cơ sở dữ liệu
            + cập nhật trạng thái đã thanh toán chuyển sang trạng thái giao hàng cho user
            + thông báo cho chủ sử hữu để giao hàng: cho phép tối đa 15 ngày để chuyển hàng tới cho người mua
                - quá hạn:
                    + đầu tiên thông báo cho cả hai đã quá thời gian giao giao hàng
                    + người dùng chọn hai cách:
                        - một gọi cho người bán: (không gửi api lên)
                        - hai gửi yêu cầu hệ thống hoàn tiền
                - Người mua bấm đã nhận hàng và người  bán đã nhấn đã gửi hàng
                    + trả tiền cho người mua
                - Người mua không đồng ý
                    - liên hệ với người bán
                    - yêu cầu hoàn trả hàng trong vòng 15 ngày nếu quá sẽ nhả tiền cho người mua
                       + người sở hữu nhận đc hàng
                       + return tiền cho khách hàng
    -: là các trường hợp khác
    +: là hành động tiếp theo
"""
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import *

from .baseview import BaseViewAPI
from ..models import Transaction, AuctionItem
from ..serializers import TransactionSerializer, TransactionCreateSerializer
from ..vnpay import vnpay


class PayViewSet(GenericViewSet, ListAPIView, BaseViewAPI):
    queryset = Transaction.objects.filter(active=True)
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    # def get_permissions(self):
    #     if self.action in ["offer", ]:
    #         return [permissions.IsAuthenticated(), ]
    #     return [permissions.AllowAny()]
    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(auction_item__receiver_id=self.request.user.pk)
        return self.queryset

    @action(methods=["GET"], url_path="info-payment/(?P<auction_item_id>[a-z0-9]+)", detail=False)
    def get_info_pay(self, request, auction_item_id, **kwargs):
        """
            nâng cao trả dữ liệu theo phương thức thanh toán tùy chọn

        """
        # chưa kiểm tra tính hợp lệ của hóa đơn,đổi tiền tệ
        try:
            instance_auction_item: AuctionItem = AuctionItem.objects.get(id=auction_item_id)
            # kiểm tra hóa đơn có tồn tại hay không và kiểm tra user đang đăng nhập hiện tại có phải user chiến thắng không
            if instance_auction_item.is_paid():
                return Response({"error": "Hóa đơn được thanh toán"})
            # if instance_auction_item.
            if instance_auction_item.receiver.pk is not request.user.pk:
                return Response({"error": "Xin lỗi. Bạn không phải là người chiến thắng"},
                                status=status.HTTP_404_NOT_FOUND)
            if Transaction.objects.filter(auction_item_id=instance_auction_item.pk).exists():
                return Response({"error": "Hóa đơn đã được thanh toán"})

            if settings.DEBUG is False:
                client_id = settings.PAYPAL_PRODUCT.get('PAYPAL_RECEIVED', None).get("client_id", None)
            else:
                client_id = settings.PAYPAL_SANDBOX.get('PAYPAL_RECEIVED', None).get("client_id", None)

            payload = {
                'amount': {
                    'current_code': 'USD',
                    'value': round(instance_auction_item.price_received / 23000000, 2)
                },
                'custom_id': "Thanh toán đấu giá " + instance_auction_item.post.title,
                'client_id': client_id
            }
            return Response(payload, status=status.HTTP_200_OK)
        except AuctionItem.DoesNotExist:
            return Response({"error": "Mã hóa đơn không hợp lệ"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["POST"], url_path="paypal/result", detail=False)
    def paypal_result(self, request, **kwargs):
        # print("data", request.data)
        result = {
            # "buyer": request.user.pk,
            "order_id": request.data.get("id", None),
            "amount": request.data.get("purchase_units", None)[0].get("amount", None).get("value", None),
            "message": request.data.get("purchase_units", None)[0].get("custom_id"),
            "status": Transaction.COMPLETED,
            "currency_code": request.data.get("purchase_units", None)[0].get("amount", None).get("currency_code", None),
            "auction_item": request.data.get("auction_item_id", None),
            "created_date": request.data.get("create_time", None),
            "update_date": request.data.get("update_time", None)
        }
        serializer = TransactionCreateSerializer(data=result)
        serializer.is_valid(raise_exception=True)
        instance: Transaction = serializer.save()
        # print("result", result)
        instance.auction_item.status = AuctionItem.NOT_YET_SHIPPED
        instance.auction_item.save()

        message_buyer = "Bạn đã thanh toán thành công sản phẩm đấu giá trong bài viết {title}." \
                        "Sản phẩm sẽ được chuyển tới bạn sớm nhất".format(
            title=instance.auction_item.post.title)
        message_seller = "Người dùng {full_name} đã thanh toán sản phẩm đấu giá {title}." \
                         "Chuyền hàng cho người mua để nhận được tiền".format(
            full_name=request.user.get_full_name(),
            title=instance.auction_item.post.title)
        self.add_notification("Thanh toán thành công",
                              user=request.user,
                              message=message_buyer,
                              url="order/" + str(instance.pk)
                              )
        self.add_notification("Người dùng đã thanh toán",
                              user=instance.auction_item.post.user,
                              message=message_seller
                              )

        request.user.email_user(subject="[Charity Social Network][Payment]",
                                message=message_buyer + "\n" + instance.__str__(),
                                )
        instance.auction_item.post.user.email_user(subject="[Charity Social Network][Payment]",
                                                   message=message_seller + "\n" + instance.__str__(),
                                                   )
        # print(instance.auction_item)
        return Response(TransactionSerializer(instance).data, status=status.HTTP_200_OK)
