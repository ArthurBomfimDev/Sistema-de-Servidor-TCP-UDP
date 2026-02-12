import socket
import threading


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


HOST = "0.0.0.0"
PORT = 5555

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Cliente UDP conectando em {HOST}:{PORT}")

thread_recebe = threading.Thread(target=recebe_mensagem, args=[cliente])
thread_recebe.start()

while True:
    mensagem = input()
    cliente.sendto(mensagem.encode("utf-8"), (HOST, PORT))
