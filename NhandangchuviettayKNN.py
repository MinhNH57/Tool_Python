import cv2
import numpy as np

# Đọc ảnh
img = cv2.imread("C:/Users/Dell/Desktop/Tool_Python/Data/digits.png", 0)

cells = [np.hsplit(row, 100) for row in np.vsplit(img, 50)]  # 50 hàng, 100 cột
x = np.array(cells)


train = x[:, :50].reshape(-1, 400).astype(np.float32)  # Lấy 50 cột đầu
test = x[:, 50:100].reshape(-1, 400).astype(np.float32)  # Lấy 50 cột sau


k = np.arange(10)  # Các nhãn từ 0 đến 9
train_label = np.repeat(k, 250)[:, np.newaxis]  # Mỗi số lặp lại 250 lần

train_label = train_label.reshape(-1, 1)

print(f"train_label.shape: {train_label.shape}")  

# In kích thước dữ liệu và nhãn trước khi huấn luyện
print(f"train.shape: {train.shape}")        # Nên là (2500, 400)
print(f"train_label.shape: {train_label.shape}")  # Nên là (2500, 1)

# In một vài mẫu và nhãn mẫu để kiểm tra
print(f"train[0]: {train[0]}") 
print(f"train_label[0]: {train_label[0]}")
print(f"train[1]: {train[1]}") 
print(f"train_label[1]: {train_label[1]}")

# Tạo mô hình KNN và huấn luyện
knn = cv2.ml.KNearest_create()
success = knn.train(train, cv2.ml.ROW_SAMPLE, train_label)

if success:
    print("Huấn luyện thành công!")
else:
    print("Huấn luyện thất bại!")

# Dự đoán trên tập kiểm tra
ret, result, neighbours, dist = knn.findNearest(test, k=5)

# In kết quả
print(f"Kết quả: {result[:10]}")        # In 10 kết quả đầu tiên
print(f"Lân cận: {neighbours[:10]}")   # In 10 hàng lân cận
print(f"Khoảng cách: {dist[:10]}")     # In 10 hàng khoảng cách
