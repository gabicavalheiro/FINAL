import socket
import threading
import subprocess
import re
from datetime import datetime

def get_ipconfig():
    """Função que executa o ipconfig no servidor e retorna as informações relevantes"""
    try:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Usando expressões regulares para encontrar o IPv4 e Gateway
            ipv4_pattern = r"Endereço IPv4[\.\s]*: ([\d\.]+)"
            gateway_pattern = r"Gateway padrão[\.\s]*: ([\d\.]+)"
            
            ipv4 = re.search(ipv4_pattern, result.stdout)
            gateway = re.search(gateway_pattern, result.stdout)

            ip_info = ""
            if ipv4:
                ip_info += f"Endereço IPv4: {ipv4.group(1)}\n"
            if gateway:
                ip_info += f"Gateway padrão: {gateway.group(1)}"
            
            return ip_info
        else:
            return "Erro ao executar o comando ipconfig."
    except Exception as e:
        return f"Ocorreu um erro ao tentar obter o ipconfig: {e}"

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
            if mensagem_cliente.lower() == 'ipconfig':
                resposta_servidor = get_ipconfig()  # Chama a função de ipconfig
            elif mensagem_cliente.lower() == 'hora':
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
