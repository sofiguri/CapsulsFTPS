import socket
import threading

clients = {}
addresses = {}


def handle_client(client, addr):
    print(f"Соединение установлено с {addr}")
    user_name = client.recv(1024).decode("utf-8")

    addresses[addr] = user_name
    clients[user_name] = client

    while True:
        word = client.recv(1024).decode("utf-8")

        if word == "привет":
            response = "Приветствую, как я могу помочь?"
        elif word == "пока":
            response = "До свидания!"
        elif word == 'manager':
            response = '#'
        else:
            response = "Я не понимаю, попробуйте еще раз."

        client.send(bytes(response, "utf-8"))


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    port = int(input("Введите порт для сервера: "))
    server.bind((host, port))

    server.listen(5)
    print(f"Сервер запущен на порту {port}")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()


if __name__ == "__main__":
    start_server()