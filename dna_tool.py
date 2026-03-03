import socket
import argparse
import sys
import os

def send_request(sequence):
    server_address = ('127.0.0.1', 34561)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(server_address)
            s.sendall(sequence.strip().encode())
            data = s.recv(1024)
            return data.decode()
    except ConnectionRefusedError:
        return "Сервер не запущен"
    except Exception as e:
        return e

def main():
    parser = argparse.ArgumentParser(description="Проверка ДНК через асинхронный сервер.")
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-s", "--sequence", help="Проверить одну последовательность из консоли")
    input_group.add_argument("-f", "--file", help="Проверить последовательности из текстового файла (одна на строку)")
    
    parser.add_argument("-o", "--output", help="Сохранить результат в указанный файл (если не указано, выводит в консоль)")
    args = parser.parse_args()

    results = []

    if args.sequence:
        print(f"Обработка строки: {args.sequence}")
        res = send_request(args.sequence)
        results.append(f"Ввод: {args.sequence}\nОтвет: {res}")

    elif args.file:
        if not os.path.exists(args.file):
            print(f"Файл {args.file} не найден.")
            sys.exit(1)
            
        print(f"Чтение файла: {args.file}")
        with open(args.file) as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if line:
                res = send_request(line)
                results.append(f"Ввод: {line}\nОтвет: {res}")

    output_text = "\n".join(results)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_text)
        print(f"Результаты записаны в файл: {args.output}")
    else:
        print("\nРезультаты проверки:")
        print(output_text)

if __name__ == "__main__":
    main()