import asyncio
import socket
import signal
from Bio.Data import IUPACData

def is_dna(sequence):
    sequence = sequence.strip().upper()

    if len(sequence) > 20:
        return "Последовательность превышает допустимый лимит символов"
    
    if not sequence:
        return "Путая строка"

    good_simbols = set(IUPACData.ambiguous_dna_letters)
    for i in sequence:
        if i not in good_simbols:
            return "Последовательность содержит недопустимые символы"
        
    return 'Последовательность прошла проверку'

class GracefulExit(SystemExit):
    pass

def shutdown():
    raise GracefulExit()

async def handle_echo(connection, loop):
    try:
        while data := await loop.sock_recv(connection, 1024):
            decoded_data = data.decode().strip()
            print(f"Получен запрос: {decoded_data}")
        
            response = is_dna(decoded_data)  
            await loop.sock_sendall(connection, response.encode())
            print(f"Отправлено обратно: {response}")

    except Exception as e:
        print(e)

    finally:
        connection.close()

async def connection_listener(server_socket, loop, tasks):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Новое подключение от {address}")

        task = asyncio.create_task(handle_echo(connection, loop))
        tasks.append(task)

async def close_tasks(tasks):
    waiters = [asyncio.wait_for(task, 2) for task in tasks]
    for task in waiters:
        try:
            await task
        except (asyncio.exceptions.TimeoutError, asyncio.CancelledError):
            pass

async def main(tasks):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 34561))
    server_socket.listen()
    server_socket.setblocking(False)

    print("Сервер запущен")
    
    loop = asyncio.get_running_loop()
    
    for signame in {'SIGINT', 'SIGTERM'}:
        try:
            loop.add_signal_handler(getattr(signal, signame), shutdown)
        except NotImplementedError:
            pass
    
    await connection_listener(server_socket, loop, client_tasks)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client_tasks = []

    try:
        loop.run_until_complete(main(client_tasks))
    except (KeyboardInterrupt, GracefulExit):
        print("Инициирована остановка сервера")
    finally:
        try:
            all_tasks = asyncio.all_tasks(loop)
            
            for task in all_tasks:
                task.cancel()
            
            if all_tasks:
                loop.run_until_complete(asyncio.gather(*all_tasks, return_exceptions=True))
                
            loop.close()
        except Exception:
            pass

        print("Сервер полностью остановлен.")