import cv2
import pytesseract
import json
import re

img = cv2.imread("C:/Users/Dell/Pictures/Screenshots/Screenshot 2025-01-03 230015.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

boxes = pytesseract.image_to_data(img)
print(boxes)

row_dict = {}

for x, b in enumerate(boxes.splitlines()):
    if x != 0:
        b = b.split()
        if len(b) == 12:
            # Chuẩn hóa văn bản: coi 'O' và '0' như nhau
            # text = re.sub(r'[^\dO]', '', b[11]).replace('O', '0')
            text = b[11]
            row, col = int(b[7]), int(b[6])
            if row not in row_dict:
                row_dict[row] = []
            row_dict[row].append({"text": text, "x": col, "y": row, "w": int(b[8]), "h": int(b[9])})

# Sắp xếp theo tọa độ x trong từng hàng
for key in row_dict:
    row_dict[key] = sorted(row_dict[key], key=lambda k: k['x'])

final_data = []
# Đánh nhãn và phân loại
for row_index, key in enumerate(sorted(row_dict.keys())):
    col_index = 0
    for item in row_dict[key]:
        # if item["text"].isdigit() or item["text"] == "00":
        item["label"] = f"{chr(65 + row_index)}{col_index + 1}"
        col_index += 1
        # else:
        #     item["label"] = "way"
        final_data.append(item)

# Tìm giá trị lớn nhất và nhỏ nhất trong dữ liệu số
numeric_texts = [int(item["text"]) for item in final_data if item["text"].isdigit()]
if numeric_texts:
    max_ = max(numeric_texts)
    min_ = min(numeric_texts)

    for item in final_data:
        if item["text"].isdigit():
            if int(item["text"]) == max_:
                item["type"] = "vip"
            else:
                item["type"] = "normal"
else:
    max_ = min_ = None

# Ghi dữ liệu vào tệp JSON
json_path = "recognized_text.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print(f"Dữ liệu đã được lưu vào {json_path}")

# Vẽ hình chữ nhật và nhãn trên ảnh
for item in final_data:
    x, y, w, h = item["x"], item["y"], item["w"], item["h"]
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    if "label" in item and item["label"]:
        cv2.putText(img, f"{item['label']}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Hiển thị ảnh
cv2.imshow("Image with detected text", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
