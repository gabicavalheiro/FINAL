import socket

HOST = 'localhost'  # Endereço IP do servidor
PORT = 5000         # Porta que o servidor está escutando

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cliente.connect((HOST, PORT))  # Tenta se conectar ao servidor
    print('Conectado ao servidor.')
except ConnectionRefusedError:
    print('Não foi possível conectar ao servidor.')
    exit()

try:
    while True:
        mensagem = input('Você (cliente): ')  # Recebe a mensagem do cliente
        if mensagem.lower() == 'sair':
            print('Encerrando conexão.')
            break
        cliente.sendall(mensagem.encode())  # Envia a mensagem para o servidor
        
        # Recebe a resposta do servidor
        data = cliente.recv(1024)
        if not data:
            print('Conexão encerrada pelo servidor.')
            break
        
        resposta_servidor = data.decode()  # Decodifica a resposta do servidor
        print(f'Servidor: {resposta_servidor}')  # Exibe a resposta do servidor

except KeyboardInterrupt:
    print('\nConexão interrompida pelo usuário.')
finally:
    cliente.close()  # Fecha a conexão com o servidor
    print('Conexão fechada.')
