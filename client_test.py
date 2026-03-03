import socket

def run_client():
    server_address = ('127.0.0.1', 34561)
    
    try:
        while True:
            sequence = input("Последовательность: ")
                
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(server_address)
                    s.sendall(sequence.encode())
                    
                    data = s.recv(1024)
                    print(data.decode())
            except ConnectionRefusedError:
                print("Сервер не запущен")
                break
    except KeyboardInterrupt:
        print("\nЗавершение работы клиента")


if __name__ == '__main__':
    run_client()