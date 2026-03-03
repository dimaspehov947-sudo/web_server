import socket

def run_sync_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_address = ('127.0.0.1', 34561)
    server_socket.bind(server_address)
    server_socket.listen()

    print("Сервер запущен")
    
    try:
        connection, client_address = server_socket.accept()
        print(f"Подключился клиент: {client_address}")
        
        while True:
            data = connection.recv(1024)
            if not data:
                break
            
            print(f"Получено: {data.decode().strip()}")
            connection.sendall(data)
            print(f"Отправлено обратно: {data.decode()}")
        
        connection.close()

    finally:
        server_socket.close()

if __name__ == '__main__':
    run_sync_server()