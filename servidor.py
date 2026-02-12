import socket
import threading
from typing import List

from cliente import Cliente

#localhost
HOST = "0.0.0.0"
PORTA = 5555

clientes_tcp: List[Cliente] = []


def start_server():
    # executa a tarefa em uma thread, permitindo multiplos processoas ao mesmo tempo, sem prender a aplicação
    thread_tcp = threading.Thread(target=conexoes_tcp)
    thread_udp = threading.Thread(target=conexoes_udp)

    thread_tcp.start()
    thread_udp.start()

    thread_tcp.join()
    thread_udp.join()


# region TCP
def conexoes_tcp():
    # with -> é um context manager: faz a limpeza automatica -> sem ele toda vez que acaba precisa fechar a conexão manualmente, ele maneja e fecha a conexão tcp automaticamente
    # libera a porta
    with socket.socket(
        # socket.socket parametros (family, type, proto, fileno)
        # socket.AF_INET -> representa o parametro family -> Configura a familia (anfitrião) como endereço IPV4 (host, port) o host pode ser um hostname na internet ou um endereço ipv4
        socket.AF_INET,
        socket.SOCK_STREAM,
    ) as servidor_tcp:  # SOCK_STREAM -> parametro type é um enumInt -> Configura o tipo para TCP
        servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor_tcp.bind((HOST, PORTA))  # Estabelece vinculo com o host e porta
        servidor_tcp.listen()  # Escuta conexões

        print(f"[INFO] Servidor TCP iniciando {HOST}:{PORTA}")
        print("[INFO] Aguardando conexões dos clientes...")

        while True:
            cliente_socket, endereco = servidor_tcp.accept()  # aceita uma nova conexão
            cliente = Cliente(endereco[1], cliente_socket, endereco)
            name = cliente.socket.recv(1024).decode("utf-8")
            cliente.username = name
            print(
                "[CONNECT] Cliente Id: {cliente.id_usuario}, username: {cliente.username} conectado de {cliente.endereco[0]}"
            )
            clientes_tcp.append(cliente)
            thread_recebe = threading.Thread(target=recebe_mensagem_tcp, args=[cliente])
            thread_recebe.start()


def recebe_mensagem_tcp(cliente: Cliente):
    # estabelece timeout de 30 segundos o cliente tem esse tempo para mandar mensagem se não é desconectado
    cliente.socket.settimeout(30)
    while True:
        try:
            mensagem = cliente.socket.recv(1024)  # Lê até 1024 bytes
            if not mensagem:
                cliente.socket.close()
                clientes_tcp.remove(cliente)
                print(
                    f"[DISCONNECT] Cliente Id: {cliente.id_usuario}, username: {cliente.username} desconectado"
                )
            else:
                mensagem = f"[MESSAGE] {cliente.username}: {mensagem.decode("utf-8")}"
                print(mensagem)
                cliente.socket.send(
                    f"[MESSAGE] ACK - ID: {cliente.id_usuario}".encode("utf-8")
                )
        except socket.timeout:
            clientes_tcp.remove(cliente)
            print(f"[TIMEOUT] Cliente {cliente.id_usuario} removido por inatividade")
            cliente.socket.send("[TIMEOUT] Removido por inatividade".encode("utf-8"))
            break
        except Exception as ex:
            print(ex)
            break


# endregion


# region UDP
def conexoes_udp():
    with socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM
    ) as servidor_udp:  # SOCK_DGRAM -> parametro type é um enumInt -> Configura o tipo para UDP
        servidor_udp.bind((HOST, PORTA))  # Estabelece vinculo com o host e porta

        print(f"[INFO] Servidor UDP iniciando {HOST}:{PORTA}")
        print("[INFO] Aguardando conexões dos clientes...")

        while True:
            # UDP NÃO TEM ACCEPT - recebe direto de qualquer um
            mensagem, endereco = servidor_udp.recvfrom(1024)

            print(
                f"[MESSAGE] (UDP) Id: {endereco[1]} HOST: {endereco[0]}: {mensagem.decode("utf-8")}"
            )

            # Não retorna ACK nem nada


# endregion

start_server()
