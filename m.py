import hmac
import hashlib
import requests
import json
from datetime import datetime

# Thông tin API từ bạn
app_id = 554
key1 = "8NdU5pG5R2spGHGhyO99HN1OhD8IQJBn"
key2 = "uUfsWgfLkRLzq6W2uNXTCxrfxs51auny"

# Tạo thông tin yêu cầu thanh toán
data = {
    "app_id": app_id,
    "app_trans_id": datetime.now().strftime("%Y%m%d_%H%M%S"),  # YYYYMMDD_HHmmss
    "app_user": "user123",  # Mã người dùng duy nhất
    "amount": 100000,  # Số tiền (đơn vị: VND)
    "description": "Thanh toán đơn hàng #12345",  # Mô tả giao dịch
    "bank_code": "zalopayapp",  # Mã ngân hàng
    "callback_url": "https://yourdomain.com/callback",  # URL nhận callback
    "embed_data": "{}",  # Dữ liệu bổ sung
    "item": "[]"  # Danh sách sản phẩm
}

# Tạo chuỗi dữ liệu để ký HMAC
data_string = f"{data['app_id']}|{data['app_trans_id']}|{data['app_user']}|{data['amount']}|{data['description']}|{data['bank_code']}|{data['callback_url']}|{data['embed_data']}|{data['item']}"
mac = hmac.new(bytes(key1, 'utf-8'), bytes(data_string, 'utf-8'), hashlib.sha256).hexdigest()
data['mac'] = mac  # Thêm chữ ký MAC vào dữ liệu

# Gửi yêu cầu tới API
url = "https://sandbox.zalopay.vn/v2/createorder"  # URL Sandbox
response = requests.post(url, json=data)

# Xử lý kết quả
print("Response status:", response.status_code)
print("Response body:", response.json())
