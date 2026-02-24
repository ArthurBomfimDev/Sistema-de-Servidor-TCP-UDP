import os
import random
import socket
import threading
import time

# Configurações do Alvo
ALVO_IP = os.getenv("ALVO_IP", "127.0.0.1")
ALVO_PORTA = int(os.getenv("ALVO_PORTA", "5555"))

# Solicitar configurações ao usuário
print("\n" + "=" * 60)
print("  TESTE DE ESTRESSE TCP")
print("=" * 60)
print(f"Alvo: {ALVO_IP}:{ALVO_PORTA}")
print("=" * 60)

try:
    TOTAL_CLIENTES = int(input("Número de clientes simultâneos: "))
    MENSAGENS_POR_CLIENTE = int(input("Mensagens por cliente: "))
except ValueError:
    print("Valores inválidos, usando padrões.")
    TOTAL_CLIENTES = 1
    MENSAGENS_POR_CLIENTE = 1

# Mensagens variadas para simular tráfego real
MENSAGENS_EXEMPLO = [
    "Teste de carga TCP",
    "Mensagem de stress test",
    "Validando resiliência do servidor",
    "Conexão persistente ativa",
    "Simulando tráfego real",
    "ACK esperado do servidor",
    "Teste FULLTIME",
]


def simular_cliente(id_cliente):
    username = f"Bot_{id_cliente}"
    try:
        # 1. Conexão inicial
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.settimeout(10)  # Timeout de rede do bot
        cliente.connect((ALVO_IP, ALVO_PORTA))

        # 2. Envio do Username (Handshake que seu servidor espera)
        cliente.send(username.encode("utf-8"))
        time.sleep(0.1)

        for i in range(MENSAGENS_POR_CLIENTE):
            # Mensagem variada para simular tráfego real
            mensagem_base = random.choice(MENSAGENS_EXEMPLO)
            payload = f"[{username}] {mensagem_base} #{i}"

            # Envia a carga de dados
            cliente.send(payload.encode("utf-8"))

            # --- O PULO DO GATO: Esperar o ACK ---
            try:
                # O bot agora fica parado aqui até o servidor mandar o "[MESSAGE] ACK..."
                resposta = cliente.recv(1024).decode("utf-8")
                # Opcional: print(f"[{username}] Recebeu: {resposta}")
            except socket.timeout:
                print(f"[AVISO] {username} não recebeu ACK da mensagem {i}")

            # Simula um intervalo entre transmissões (comum em rastreadores)
            time.sleep(random.uniform(0.1, 0.5))

        # 3. Encerramento amigável
        print(f"[FINALIZADO] {username} concluiu as tarefas.")
        time.sleep(0.5)  # Margem de segurança
        cliente.close()

    except Exception as e:
        print(f"[ERRO NO BOT {id_cliente}] {e}")


# --- Orquestrador do Stress ---
threads = []
print(f"\nAlvo: {ALVO_IP}:{ALVO_PORTA}")
print(f"Clientes: {TOTAL_CLIENTES}")
print(f"Mensagens por cliente: {MENSAGENS_POR_CLIENTE}")
print(f"Total de mensagens: {TOTAL_CLIENTES * MENSAGENS_POR_CLIENTE}")
print(f"{'='*60}\n")

start_time = time.time()

for i in range(TOTAL_CLIENTES):
    t = threading.Thread(target=simular_cliente, args=(i + 1,))
    threads.append(t)
    t.start()
    # Pequeno delay para não sobrecarregar o processador local ao criar as threads
    time.sleep(0.02)

for t in threads:
    t.join()

end_time = time.time()
duration = end_time - start_time

print(f"\n{'='*60}")
print("  TESTE CONCLUÍDO COM SUCESSO")
print(f"{'='*60}")
print(f"  Tempo total: {duration:.2f} segundos")
print(f"  Mensagens enviadas: {TOTAL_CLIENTES * MENSAGENS_POR_CLIENTE}")
print(f"  Taxa: {(TOTAL_CLIENTES * MENSAGENS_POR_CLIENTE) / duration:.2f} msg/s")
print(f"{'='*60}\n")
