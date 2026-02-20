# 🚀 Guia Rápido - Docker

## 📋 Início Rápido

### Opção 1: Menu Interativo (RECOMENDADO)
```bash
./docker-menu.sh
```

### Opção 2: Comandos Manuais

#### 1. Iniciar Servidor
```bash
docker compose up -d
```

#### 2. Ver Logs do Servidor (outro terminal)
```bash
docker compose logs -f servidor
```

#### 3. Criar Clientes TCP (terminais separados)
```bash
# Terminal 1
./run-cliente-tcp.sh Arthur

# Terminal 2
./run-cliente-tcp.sh Maria

# Terminal 3
./run-cliente-tcp.sh João
```

#### 4. Criar Cliente UDP
```bash
./run-cliente-udp.sh
```

#### 5. Testes de Estresse
```bash
# TCP (5000 clientes, 5 mensagens)
docker compose --profile stress-test run --rm teste-estresse-tcp

# UDP (500 clientes, 100 mensagens)
docker compose --profile stress-test run --rm teste-estresse-udp

# Personalizado
docker compose --profile stress-test run --rm \
  -e TOTAL_CLIENTES=1000 \
  -e MENSAGENS_POR_CLIENTE=10 \
  teste-estresse-tcp
```

#### 6. Parar Servidor
```bash
docker compose down
```

---

## 💡 Exemplo Prático

**Terminal 1 - Servidor:**
```bash
docker compose up servidor
```

**Terminal 2 - Cliente Arthur:**
```bash
./run-cliente-tcp.sh Arthur
# Digite: Olá servidor!
```

**Terminal 3 - Cliente Maria:**
```bash
./run-cliente-tcp.sh Maria
# Digite: Tudo bem?
```

**Resultado no Terminal 1:**
```
[CONNECT] Cliente Id: 12345, username: Arthur conectado
[MESSAGE] Arthur: Olá servidor!
[CONNECT] Cliente Id: 12346, username: Maria conectado
[MESSAGE] Maria: Tudo bem?
```

---

## 🛠️ Comandos Úteis

```bash
# Status dos containers
docker compose ps

# Uso de recursos
docker stats

# Reconstruir imagens
docker compose build

# Limpar tudo
docker compose down -v
docker system prune -f
```

---

## ⚡ Dicas

- Servidor separado = logs limpos
- Cada cliente em terminal próprio = controle total
- Use nomes descritivos nos clientes TCP
- Ctrl+C para sair de um cliente
- Use `docker compose` (sem hífen)
