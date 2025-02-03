import socket

def start_server():
    host = '0.0.0.0'  # Lắng nghe trên tất cả các giao diện mạng
    port = 12345  # Cổng để lắng nghe

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Listening on {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    while True:
        command = input("Enter command: ")
        if command.lower() == 'exit':
            conn.send(command.encode('utf-8'))
            break

        conn.send(command.encode('utf-8'))
        response = conn.recv(4096).decode('utf-8')
        print(response)

    conn.close()

if __name__ == "__main__":
    start_server()
