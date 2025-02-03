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
    lower_orange = np.array([0, 100, 150])  
    upper_orange = np.array([25, 255, 255])

    # Tạo mặt nạ chỉ cho màu cam
    mask_orange = cv2.inRange(hsv_image, lower_orange, upper_orange)

    # Hiển thị mask màu cam để kiểm tra
    cv2.imshow("Original Image", image)
    cv2.imshow("Orange Mask", mask_orange)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Chuyển sang ảnh xám và làm mờ
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Phát hiện cạnh với tham số mới
    edges = cv2.Canny(blurred, 50, 150)  # Có thể điều chỉnh ngưỡng này

    # Tìm các contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blocks = []
    grouped_blocks_by_y = defaultdict(list)

    # Xử lý các contours để xác định các khu vực chứa ghế
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Giảm kích thước khối tối thiểu để nhận diện nhiều khối hơn
        if w > 30 and h > 30:  # Thử giảm ngưỡng này từ 50 xuống 30
            block_image = image[y:y+h, x:x+w]
            block_hsv = cv2.cvtColor(block_image, cv2.COLOR_BGR2HSV)

            block_mask_orange = cv2.inRange(block_hsv, lower_orange, upper_orange)

            block_color = None
            if np.sum(block_mask_orange) > 0:  # Nếu có màu cam trong khối
                block_color = "Orange"

            if block_color:
                grouped_blocks_by_y[y].append({
                    "X": x,
                    "Y": y,
                    "Width": w,
                    "Height": h,
                    "Block_Color": block_color
                })

    # Nhóm các khối liền nhau (cùng hàng hoặc cột, không có khoảng trống)
    def is_adjacent(block1, block2):
        # Nếu khối nằm gần nhau trong cùng một hàng, không cần kiểm tra khoảng trống
        return abs(block1['Y'] - block2['Y']) <= 10  # Các khối cùng hàng sẽ có sự chênh lệch Y nhỏ

    grouped_blocks = []
    current_group = []

    # Duyệt qua các khối và nhóm chúng lại nếu chúng gần nhau trong cùng một hàng
    for y, blocks_in_row in sorted(grouped_blocks_by_y.items()):
        blocks_in_row_sorted = sorted(blocks_in_row, key=lambda block: block["X"]) 

        for block in blocks_in_row_sorted:
            if not current_group:
                current_group.append(block)
            else:
                # Kiểm tra nếu khối này gần khối trước đó thì nhóm lại
                if is_adjacent(current_group[-1], block):
                    current_group.append(block)
                else:
                    grouped_blocks.append(current_group)
                    current_group = [block]

        # Thêm nhóm còn lại vào danh sách
        if current_group:
            grouped_blocks.append(current_group)
            current_group = []

    # Danh sách tên hàng
    row_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'] 
    result = []
    row_index = 0

    # Duyệt qua các nhóm và gán tên cho ghế
    for group in grouped_blocks:
        row_name = row_names[row_index]
        seat_index = 1
        for block in group:
            if block["Block_Color"] == "Orange":  # Chỉ xử lý khối màu cam
                cell_name = f"{row_name}{seat_index}"  # Tạo tên ghế như A1, A2, ...
                block["Cell_Name"] = cell_name
                seat_index += 1  # Tăng chỉ số ghế cho lần lặp tiếp theo
            result.append(block)

            # Vẽ viền đỏ bao quanh khối
            cv2.rectangle(image, (block["X"], block["Y"]), 
                          (block["X"] + block["Width"], block["Y"] + block["Height"]), 
                          (0, 0, 255), 2)  # Màu đỏ (0, 0, 255) và độ dày đường viền là 2

        row_index += 1

    # Hiển thị ảnh với các khối đã được vẽ viền đỏ
    cv2.imshow("Seating Plan with Detected Blocks", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result

# Gọi hàm và truyền đường dẫn ảnh
image_path = "C:/Users/Dell/Pictures/Screenshots/Screenshot 2024-12-29 142852.png"
seating_plan = process_seating_plan(image_path)

# Lưu kết quả vào tệp JSON
output_path = "blocks.json"
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(seating_plan, json_file, ensure_ascii=False, indent=4)

print(f"Kết quả đã được lưu vào {output_path}")
