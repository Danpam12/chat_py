import socket
import threading

# Defina o host e a porta para o servidor
HOST = 'localhost'
PORT = 5000

# Cria um socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Função para lidar com as mensagens recebidas do servidor
def receive_messages():
    while True:
        try:
            mensagem = client_socket.recv(1024).decode('utf-8')
            print(mensagem)
        except Exception as e:
            print(f'Erro: {str(e)}')
            client_socket.close()
            break

# Função principal para enviar mensagens ao servidor
def send_message():
    while True:
        mensagem = input()
        client_socket.send(mensagem.encode('utf-8'))

# Inicia as threads para receber e enviar mensagens
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()