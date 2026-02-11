import os
import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

nome = ""
while True:
    nome = input("Digite seu nome de usuario: ")
    if nome != None and nome != "":
        break
    else:
        print("[ERRO] nome digitado invalido!")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Concta-se ao servidor
    cliente.connect((HOST, PORT))
    print("Conectado ao servidor!")
    cliente.send(nome.encode("utf-8"))
except Exception as ex:
    print(f"[ERRO] CONEXÃO COM SERVIDOR FALHOU: {ex}")
    exit()


def recebe_mensagem(servidor):
    while True:
        try:
            mensagem = servidor.recv(1024).decode("utf-8")
            if mensagem != None and mensagem != "":
                if str.startswith(mensagem, "[TIMEOUT]"):
                    print(mensagem)
                    os._exit(-1)

                print(mensagem)
        except Exception as ex:
            print(f"[ERRO] {ex}")
            break


thread_recebe = threading.Thread(target=recebe_mensagem, args=[cliente])
thread_recebe.start()

while True:
    mensagem = input("")
    try:
        cliente.send(mensagem.encode("utf-8"))
    except Exception:
        print("* Erro ao enviar mensagem: {ex}")
        break
