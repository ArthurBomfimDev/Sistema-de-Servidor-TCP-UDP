import socket
import threading
import time
import zlib  # Biblioteca utilizada para decompactar de mensagenss (UDP)
from typing import List

from cliente import Cliente

# localhost
HOST = "0.0.0.0"
PORTA = 5555

# Utiliza lock para evitar erro de duas threads editarem a lista oa mesmo tempo
clientes_lock = threading.Lock()
clientes_tcp: List[Cliente] = []


def start_server():
    # executa a tarefa em uma thread, permitindo multiplos processoas ao mesmo tempo, sem prender a aplicação
    thread_tcp = threading.Thread(target=conexoes_tcp)
    thread_udp = threading.Thread(target=conexoes_udp)

    thread_tcp.start()
    thread_udp.start()

    # Mantem o processo principal vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[INFO] Desligando o servidor...")


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
        # Permite reabrir o servidor na mesma porta imeditamente
        servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor_tcp.bind((HOST, PORTA))  # Estabelece vinculo com o host e porta
        servidor_tcp.listen()  # Escuta conexões

        print(f"[INFO] Servidor TCP iniciando {HOST}:{PORTA}")
        print("[INFO] Aguardando conexões dos clientes...")

        while True:
            try:
                cliente_socket, endereco = (
                    servidor_tcp.accept()
                )  # aceita uma nova conexão
                cliente = Cliente(endereco[1], cliente_socket, endereco)
                name = cliente.socket.recv(1024).decode("utf-8")
                cliente.username = name
                print(
                    f"[CONNECT] Cliente Id: {cliente.id_usuario}, username: {cliente.username} conectado de {cliente.endereco[0]}"
                )

                # utilizando o look para adicionar os clientes na lista
                with clientes_lock:
                    clientes_tcp.append(cliente)

                thread_recebe = threading.Thread(
                    target=recebe_mensagem_tcp, args=[cliente]
                )
                thread_recebe.start()
            except Exception as ex:
                print(f"[ERRO] Falha ao aceitar conexões: {ex}")


def recebe_mensagem_tcp(cliente: Cliente):
    # estabelece timeout de 30 segundos o cliente tem esse tempo para mandar mensagem se não é desconectado
    cliente.socket.settimeout(30)

    try:
        while True:
            try:
                mensagem = cliente.socket.recv(1024)  # Lê até 1024 bytes
                if not mensagem:
                    # Remove o cliente no bloco finally
                    break

                # Decodifica e printa a mensagem do cliente
                print(f"[MESSAGE] {cliente.username}: {mensagem.decode('utf-8')}")

                # Envia o ack de confirmação ao cliente
                cliente.socket.send(
                    f"[MESSAGE] ACK - ID: {cliente.id_usuario}".encode("utf-8")
                )

            except socket.timeout:

                print(
                    f"[TIMEOUT] Cliente {cliente.id_usuario} removido por inatividade"
                )
                # Envia a mensagem pro cliente informando o motivo da desconexão TIMEOUT
                cliente.socket.send(
                    "[TIMEOUT] Removido por inatividade".encode("utf-8")
                )
                break

            except (ConnectionResetError, BrokenPipeError):

                print(f"[INFO] Cliente {cliente.username} desconectou antes do ACK.")
                break  # Sai do loop e limpa os recursos no finally

            except Exception as ex:

                print(f"[ERRO] {ex}")
                break

    except Exception as ex:
        # Se for Errno 9, ignoramos pois o socket já foi fechado propositalmente
        if getattr(ex, "errno", None) != 9:
            print(f"[ERRO] {cliente.username}: {ex}")
    finally:
        # Limpeza centralizada - Removendo os clientes da lista e fechando o socket
        with clientes_lock:
            if cliente in clientes_tcp:
                clientes_tcp.remove(cliente)
        try:
            cliente.socket.close()
        except:
            # Provavelmente o socket ja foi encerrado
            pass

        print(
            f"[DISCONNECT] Cliente Id: {cliente.id_usuario}, username: {cliente.username} foi desconectado"
        )


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

            mensagem_descompactada = zlib.decompress(mensagem).decode("utf-8")

            print(
                f"[MESSAGE] (UDP) Id: {endereco[1]} HOST: {endereco[0]}: {mensagem_descompactada}"
            )

            # Não retorna ACK nem nada


# endregion

start_server()
