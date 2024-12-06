import socket
import threading
from datetime import datetime

def get_hora():
    """Retorna a hora atual do servidor"""
    return f"A hora atual é: {datetime.now().strftime('%H:%M:%S')}"

def handle_client(conn, addr):
    print(f'Conexão estabelecida com {addr}')
    try:
        while True:
            data = conn.recv(1024)  # Recebe dados do cliente
            if not data:
                print(f'Conexão encerrada pelo cliente {addr}')
                break
            mensagem_cliente = data.decode()  # Decodifica a mensagem do cliente
            print(f'Cliente {addr}: {mensagem_cliente}')

            # Responde de acordo com o comando do cliente
            if mensagem_cliente.lower() == 'hora':
                resposta_servidor = get_hora()  # Chama a função de hora
            elif mensagem_cliente.lower().startswith('echo'):
                # Echo: Retorna a mesma mensagem do cliente
                resposta_servidor = mensagem_cliente[5:]  # Removendo "echo " da frente
            else:
                resposta_servidor = "Comando não reconhecido."

            # Envia a resposta ao cliente
            conn.sendall(resposta_servidor.encode())
    except ConnectionResetError:
        print(f'Conexão com {addr} foi encerrada abruptamente.')
    finally:
        conn.close()
        print(f'Conexão fechada com {addr}')

HOST = ''  # Escuta em todas as interfaces de rede disponíveis
PORT = 5000  # Porta para escutar as conexões

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print(f'Servidor escutando na porta {PORT}...')

while True:
    conn, addr = servidor.accept()  # Aceita uma nova conexão
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()  # Cria uma thread para o cliente
    print(f'Clientes ativos: {threading.active_count() - 1}')
