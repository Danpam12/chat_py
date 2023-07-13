import socket
import threading

# Defina o host e a porta para o servidor
HOST = 'localhost'
PORT = 5000

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# Lista para armazenar as conexões dos clientes
clientes = []
# Dicionário para mapear os sockets dos clientes aos seus nomes
nomes_clientes = {}

# Função para lidar com as mensagens dos clientes
def handle_client(client_socket, client_address):
    while True:
        try:
            # Recebe a mensagem do cliente
            mensagem = client_socket.recv(1024).decode('utf-8')

            if mensagem.startswith('/nome'):
                nome = mensagem.split()[1]
                clientes.append(client_socket)
                nomes_clientes[client_socket] = nome
                mensagem_envio = f'Bem-vindo(a), {nome}!'
                client_socket.send(mensagem_envio.encode('utf-8'))
            elif mensagem.startswith('/privado'):
                dados_mensagem = mensagem.split()
                if len(dados_mensagem) >= 3:
                    nome_destinatario = dados_mensagem[1]
                    mensagem_privada = ' '.join(dados_mensagem[2:])
                    destinatario = None
                    for sock, nome in nomes_clientes.items():
                        if nome == nome_destinatario:
                            destinatario = sock
                            break
                    if destinatario is not None:
                        mensagem_envio = f'Mensagem privada de {nomes_clientes.get(client_socket)}: {mensagem_privada}'
                        destinatario.send(mensagem_envio.encode('utf-8'))
                    else:
                        mensagem_envio = f'O usuário {nome_destinatario} não existe.'
                        client_socket.send(mensagem_envio.encode('utf-8'))
                else:
                    mensagem_envio = 'Formato inválido. Use /privado <nome_destinatario> <mensagem>'
                    client_socket.send(mensagem_envio.encode('utf-8'))
            else:
                remetente = nomes_clientes.get(client_socket)
                mensagem_envio = f'{remetente}: {mensagem}'
                broadcast(mensagem_envio.encode('utf-8'))

        except Exception as e:
            print(f'Erro: {str(e)}')
            clientes.remove(client_socket)
            remetente = nomes_clientes.pop(client_socket, None)
            client_socket.close()
            broadcast(f'Usuário {remetente} saiu do chat.'.encode('utf-8'))
            break



# Função para enviar mensagens a todos os clientes conectados
def broadcast(mensagem):
    for client in clientes:
        client.send(mensagem)

# Função principal para iniciar o servidor
def start_server():
    print('Servidor iniciado. Aguardando conexões...')

    while True:
        client_socket, client_address = server_socket.accept()
        clientes.append(client_socket)
        print(f'Cliente {client_address} conectado.')
        client_socket.send('Informe seu nome: /nome <seu_nome>'.encode('utf-8'))
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

start_server()