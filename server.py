import threading
import socket


host = '127.0.0.1'
port = 23322

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames = []

def brodcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            brodcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            brodcast(f"{nickname} left the chat!!" .encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address= server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f'Nickname of client is {nickname}!')
        brodcast(f'{nickname} joined the chat!!'.encode('ascii'))
        client.send(f'connected to the server'.encode('ascii'))

        tread =threading.Thread(target=handle, args=(client,))

        tread.start()

print("server is listening....")
receive()