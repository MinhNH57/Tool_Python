import pyodbc
from faker import Faker
import random

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-RTLBH4I\SQLEXPRESS;'
    'DATABASE=StockApp;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

fake = Faker()

def generate_data():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=90),
        "balance": round(random.uniform(1000, 100000), 2)
    }

# Chèn dữ liệu vào bảng
table_name = "Stocks"
num_records = 100  # Số bản ghi cần tạo

for _ in range(num_records):
    data = generate_data()
    cursor.execute(f"""
        INSERT INTO {table_name} (name, email, phone, dob, balance)
        VALUES (?, ?, ?, ?, ?)
    """, data["name"], data["email"], data["phone"], data["dob"], data["balance"])

conn.commit()
cursor.close()
conn.close()

print(f"{num_records} bản ghi đã được chèn vào bảng {table_name}.")