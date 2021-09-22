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


