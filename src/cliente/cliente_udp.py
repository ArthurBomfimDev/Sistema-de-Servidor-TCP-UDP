import os
import socket
import threading
import zlib  # Biblioteca que permite a compressão

# Obtém o IP e Porta via variável de ambiente (Docker) ou usa localhost por padrão (Local)
HOST = os.getenv("ALVO_IP", "127.0.0.1")
PORT = int(os.getenv("ALVO_PORTA", "5555"))


# Função para receber mensagem rodada em outra thread
def recebe_mensagem(cliente: socket):
    while True:
        try:
            mensagem, endereco = cliente.recvfrom(1024)
            print(endereco)
            if mensagem != None and mensagem != "":
                print(f"[MESSAGE] {mensagem.decode('utf-8')}")
        except Exception as ex:
            print(f"* Erro Interno: {ex}")
            break


cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Cliente UDP conectando em {HOST}:{PORT}")

thread_recebe = threading.Thread(target=recebe_mensagem, args=[cliente])
thread_recebe.start()

while True:
    mensagem = input()
    # Compressão
    mensagem_compressada = zlib.compress(mensagem.encode("utf-8"))
    # Envio
    cliente.sendto(mensagem_compressada, (HOST, PORT))
