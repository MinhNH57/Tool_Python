import cv2
import json
import numpy as np
from collections import defaultdict

def process_seating_plan(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return json.dumps({"error": "Không thể đọc ảnh. Vui lòng kiểm tra lại đường dẫn!"})

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Định nghĩa phạm vi màu cam
    lower_orange = np.array([5, 150, 150])  
    upper_orange = np.array([25, 255, 255])

    # Định nghĩa phạm vi màu xanh lá cây đậm (mã màu #228D83)
    lower_green = np.array([35, 80, 80])  
    upper_green = np.array([85, 255, 255])

    # Định nghĩa phạm vi màu xám
    lower_gray = np.array([0, 0, 50])  # Saturation (S) thấp và Value (V) trung bình
    upper_gray = np.array([180, 50, 200])  # Bao gồm mọi giá trị Hue (H)

    # Tạo mặt nạ cho các màu cam, xanh lá cây đậm, và xám
    mask_orange = cv2.inRange(hsv_image, lower_orange, upper_orange)
    mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
    mask_gray = cv2.inRange(hsv_image, lower_gray, upper_gray)

    # Kết hợp tất cả các mặt nạ
    mask = mask_orange | mask_green | mask_gray

    # Chuyển sang ảnh xám và làm mờ
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Phát hiện cạnh
    edges = cv2.Canny(blurred, 50, 150)

    # Tìm các contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blocks = []
    grouped_blocks_by_y = defaultdict(list)

    # Xử lý các contours để xác định các khu vực chứa ghế
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w > 20 and h > 20:  # Lọc các khối nhỏ không cần thiết
            block_image = image[y:y+h, x:x+w]
            block_hsv = cv2.cvtColor(block_image, cv2.COLOR_BGR2HSV)

            block_mask_orange = cv2.inRange(block_hsv, lower_orange, upper_orange)
            block_mask_green = cv2.inRange(block_hsv, lower_green, upper_green)
            block_mask_gray = cv2.inRange(block_hsv, lower_gray, upper_gray)

            block_color = None
            if np.sum(block_mask_orange) > max(np.sum(block_mask_green), np.sum(block_mask_gray)):
                block_color = "Orange"
            elif np.sum(block_mask_green) > max(np.sum(block_mask_orange), np.sum(block_mask_gray)):
                block_color = "Green"
            elif np.sum(block_mask_gray) > max(np.sum(block_mask_orange), np.sum(block_mask_green)):
                block_color = "Gray"

            grouped_blocks_by_y[y].append({
                "X": x,
                "Y": y,
                "Width": w,
                "Height": h,
                "Block_Color": block_color
            })

    # Danh sách tên hàng
    row_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'] 
    result = []
    row_index = 0

    # Duyệt qua các hàng và cột để gán tên cho các ghế
    for y, blocks_in_row in sorted(grouped_blocks_by_y.items()):
        row_name = row_names[row_index]
        blocks_in_row_sorted = sorted(blocks_in_row, key=lambda block: block["X"]) 

        seat_index = 1 
        for block in blocks_in_row_sorted:
            if block["Block_Color"] != "Gray":  
                cell_name = f"{row_name}{seat_index}"  # Tạo tên ghế như A1, A2, ...
                block["Cell_Name"] = cell_name
                seat_index += 1  # Tăng chỉ số ghế cho lần lặp tiếp theo
            result.append(block)

        row_index += 1
    return result

# Gọi hàm và truyền đường dẫn ảnh
image_path = "C:/Users/Dell/Downloads/z6180737564350_e162a8123401a0c137712d02d8c0e0ea.jpg"
seating_plan = process_seating_plan(image_path)

# Lưu kết quả vào tệp JSON
output_path = "blocks.json"
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(seating_plan, json_file, ensure_ascii=False, indent=4)

print(f"Kết quả đã được lưu vào {output_path}")
