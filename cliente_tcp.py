import socket
import threading

# localhost
HOST = "0.0.0.0"
PORT = 5555

nome = ""
while True:
    nome = input("Digite seu nome de usuario: ")
    if nome != None and nome != "":
        break
    else:
        print("[ERRO] nome digitado invalido!")

# Cria o socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Flag/Evento que avisa a aplicação se está conectado ou não
conectado = threading.Event()


# Função utilizada para conectar/reconectar
def conectar():
    global servidor
    try:
        servidor.close()
    except:
        pass

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Concta-se ao servidor
        servidor.connect((HOST, PORT))
        servidor.send(nome.encode("utf-8"))
        print("Conectado ao servidor!")
    except Exception as ex:
        print(f"[ERRO] CONEXÃO COM SERVIDOR FALHOU: {ex}")
        exit()


# Função rodada em Thread separada utilizada para receber mensagem
def recebe_mensagem():
    while True:
        try:
            mensagem = servidor.recv(1024).decode("utf-8")
            if not mensagem:
                # Muda o estado, avisa o resto do programa que não está mais conectado com o servidor
                conectado.set()
                return
            else:
                if str.startswith(mensagem, "[TIMEOUT]"):
                    print(mensagem)
                    conectado.set()
                    print("Pressione qualquer tecla para reconectar...")
                    return
                else:
                    print(mensagem)
        except Exception as ex:
            print(f"[ERRO] {ex}")
            break


conectar()
# Configurando thread de recebimento de mensagem
thread_recebe = threading.Thread(target=recebe_mensagem)
# Iniciando a Thread
thread_recebe.start()

# loop de envio de mensagem
while True:
    if conectado.is_set():
        print("Reconectando...")
        conectar()
        conectado.clear()  # "Baixa a bandeira" para poder usar de novo
    try:
        mensagem = input("")
        servidor.send(mensagem.encode("utf-8"))
    except Exception:
        print("[ERRO] Falha ao enviar mensagem: {ex}")
        break
