from socket import *

server_name = "127.0.0.1"
server_port = 12000

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_name, server_port))

server_socket.listen(1)
print("The server is ready to receive!")

while True:
    connection_socket, addr = server_socket.accept()

    sentence = connection_socket.recv(1024).decode()
    print(sentence)
    capitalized_sentence = "Hello this is server!"
    connection_socket.send(capitalized_sentence.encode())
    connection_socket.close()
