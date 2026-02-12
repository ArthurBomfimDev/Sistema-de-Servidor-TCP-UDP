import socket
import threading

#localhost
HOST = "0.0.0.0"
PORT = 5555

nome = ""
while True:
    nome = input("Digite seu nome de usuario: ")
    if nome != None and nome != "":
        break
    else:
        print("[ERRO] nome digitado invalido!")

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Concta-se ao servidor
    servidor.connect((HOST, PORT))
    print("Conectado ao servidor!")
    servidor.send(nome.encode("utf-8"))
except Exception as ex:
    print(f"[ERRO] CONEXÃO COM SERVIDOR FALHOU: {ex}")
    exit()


def reconnect():
    global servidor
    try:
        servidor.close()
    except:
        pass

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.connect((HOST, PORT))
    servidor.send(nome.encode("utf-8"))
    print("Conectado ao servidor!")


def recebe_mensagem():
    while True:
        try:
            mensagem = servidor.recv(1024).decode("utf-8")
            if mensagem != None and mensagem != "":
                if str.startswith(mensagem, "[TIMEOUT]"):
                    print(mensagem)
                    input("Aperte qualquer tecla para reconectar...")
                    reconnect()
                else:
                    # os._exit(-1)
                    print(mensagem)
        except Exception as ex:
            print(f"[ERRO] {ex}")
            break


thread_recebe = threading.Thread(target=recebe_mensagem)
thread_recebe.start()

while True:
    mensagem = input("")
    if mensagem == "/sair":
        servidor.send(mensagem.encode("utf-8"))
        break
    try:
        servidor.send(mensagem.encode("utf-8"))
    except Exception:
        print("* Erro ao enviar mensagem: {ex}")
        break
