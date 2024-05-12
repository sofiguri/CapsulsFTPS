import socket
import subprocess
from FSettings import User_path 


def rename(name):
    with open(User_path, "w") as file:
        file.write(str(name))


def start_client():
    global user_name
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    port = int(input("Введите порт для подключения к серверу: "))

    client.connect((host, port))

    user_name = input("Введите ваше имя: ")
    client.send(bytes(user_name, "utf-8"))

    while True:
        word = input("Введите слово: ")
        if bytes(word, "utf-8") == 'exit':
            break
        client.send(bytes(word, "utf-8"))

        response = client.recv(1024).decode("utf-8")
        if response == '#':
            rename(user_name)
            subprocess.run(["python", "FTP_Manager.py"])
        else:
            print("Ответ от сервера:", response)
