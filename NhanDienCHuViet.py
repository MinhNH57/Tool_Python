import cv2 
import pytesseract 
import json

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

img = cv2.imread("C:/Users/Dell/Pictures/Screenshots/Screenshot 2024-12-31 233209.png")

img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY) 
boxes = pytesseract.image_to_data(img)
data = []

for x , b in enumerate(boxes.splitlines()):
    if x != 0 :
        print(b)
        b = b.split()
        if(len(b) == 12):
            x , y , w, h = int(b[6]) , int(b[7]) , int(b[8]) , int(b[9])
            text = b[11]
            data.append({"text": text, "x": x, "y": y, "w": w, "h": h})
            cv2.rectangle(img , (x , y) , (x + w , h  + y) , (0,0,255) , 2)

json_path = "recognized_text.json" 
with open(json_path, 'w', encoding='utf-8') as f: 
    json.dump(data, f, ensure_ascii=False, indent=4)
print(f"Dữ liệu đã được lưu vào {json_path}")
