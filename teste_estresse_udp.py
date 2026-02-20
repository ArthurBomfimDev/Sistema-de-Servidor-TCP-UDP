import os
import random
import socket
import threading
import time
import zlib

# Configurações do Alvo
ALVO_IP = os.getenv("ALVO_IP", "127.0.0.1")
ALVO_PORTA = int(os.getenv("ALVO_PORTA", "5555"))

# Solicitar configurações ao usuário
print("\n" + "="*60)
print("  TESTE DE ESTRESSE UDP")
print("="*60)

try:
    TOTAL_CLIENTES = int(input("Número de clientes simultâneos (padrão 100): ") or "100")
    MENSAGENS_POR_CLIENTE = int(input("Mensagens por cliente (padrão 10): ") or "10")
except ValueError:
    print("Valores inválidos, usando padrões.")
    TOTAL_CLIENTES = 100
    MENSAGENS_POR_CLIENTE = 10

# Mensagens variadas para simular tráfego UDP real
MENSAGENS_EXEMPLO = [
    "Pacote UDP de teste",
    "Mensagem sem conexão",
    "Datagram stress test",
    "Fire and forget message",
    "UDP throughput test",
    "Latency measurement UDP",
    "Broadcast simulation",
]


def simular_cliente(id_cliente):
    username = f"UDP_Bot_{id_cliente}"
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cliente.connect((ALVO_IP, ALVO_PORTA))

        for i in range(MENSAGENS_POR_CLIENTE):
            # Mensagem variada para simular tráfego real
            mensagem_base = random.choice(MENSAGENS_EXEMPLO)
            payload = f"[{username}] {mensagem_base} #{i}"
            compress = zlib.compress(payload.encode("utf-8"))
            
            # Envia a carga de dados
            cliente.send(compress)

            # Simula um intervalo entre transmissões
            time.sleep(random.uniform(0.05, 0.2))

        print(f"[FINALIZADO] {username} concluiu {MENSAGENS_POR_CLIENTE} mensagens.")
        time.sleep(0.3)
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
    t = threading.Thread(target=simular_cliente, args=(i,))
    threads.append(t)
    t.start()
    # Pequeno delay para não sobrecarregar o processador local ao criar as threads
    time.sleep(0.02)

for t in threads:
    t.join()

end_time = time.time()
duration = end_time - start_time

print(f"\n{'='*60}")
print(f"  TESTE CONCLUÍDO COM SUCESSO")
print(f"{'='*60}")
print(f"  Tempo total: {duration:.2f} segundos")
print(f"  Mensagens enviadas: {TOTAL_CLIENTES * MENSAGENS_POR_CLIENTE}")
print(f"  Taxa: {(TOTAL_CLIENTES * MENSAGENS_POR_CLIENTE) / duration:.2f} msg/s")
print(f"{'='*60}\n")
