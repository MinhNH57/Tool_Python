import pyodbc
import sys

# Thông tin kết nối cơ sở dữ liệu
server = 'localhost,1433' # Địa chỉ máy chủ
database = 'DA1_Cinema01'  # Tên cơ sở dữ liệu

try:
    # Kết nối đến cơ sở dữ liệu sử dụng Windows Authentication
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes')
    cursor = conn.cursor()

    # Tên bảng và điều kiện xóa
    table_name = 'RoomLayout'  # Tên bảng cần xóa dữ liệu
    condition = "RoomId = 42069773-AB3F-41EE-227A-08DD27E11B51"  # Điều kiện để xóa dữ liệu (ví dụ xóa bản ghi có RoomId = 5)

    # Nếu có điều kiện xóa, sử dụng WHERE, nếu không thì xóa toàn bộ dữ liệu
    if condition:
        sql_query = f"DELETE FROM {table_name} WHERE {condition}"
    else:
        sql_query = f"DELETE FROM {table_name}"

    # Thực thi câu lệnh SQL
    cursor.execute(sql_query)

    # Commit các thay đổi
    conn.commit()

    print(f"Dữ liệu đã được xóa thành công từ bảng {table_name}.")

except Exception as e:
    print(f"Đã xảy ra lỗi khi xóa dữ liệu: {e}")
    if 'conn' in locals():
        conn.rollback()  # Rollback nếu có lỗi

finally:
    # Đóng kết nối
    if 'conn' in locals():
        conn.close()
