# 🚀 Guia Rápido - Docker

## 📋 Início Rápido

### Opção 1: Menu Interativo (RECOMENDADO)
```bash
./docker-menu.sh
```

Cada opção abre automaticamente em um novo terminal!

### Opção 2: Comandos Manuais

#### 1. Iniciar Servidor
```bash
docker compose up -d
```

#### 2. Ver Logs (abre em novo terminal)
```bash
./docker-menu.sh
# Escolha opção [2]
```

#### 3. Criar Clientes TCP (cada um abre em novo terminal)
```bash
./run-cliente-tcp.sh Arthur
./run-cliente-tcp.sh Maria
./run-cliente-tcp.sh João
```

#### 4. Criar Cliente UDP (abre em novo terminal)
```bash
./run-cliente-udp.sh
```

#### 5. Testes de Estresse (abrem em novo terminal)
```bash
# Via menu
./docker-menu.sh
# Escolha opção [5] para TCP ou [6] para UDP
```

#### 6. Parar Servidor
```bash
docker compose down
```

---

## 💡 Fluxo de Trabalho

**1. Execute o menu:**
```bash
./docker-menu.sh
```

**2. Escolha [1] - Iniciar Servidor**

**3. Escolha [2] - Ver Logs**
- Abre terminal com logs em tempo real

**4. Execute o menu novamente e escolha [3] - Cliente TCP**
- Digite: Arthur
- Abre novo terminal com cliente conectado

**5. Execute o menu novamente e escolha [3] - Cliente TCP**
- Digite: Maria
- Abre outro terminal com cliente conectado

**6. Digite mensagens em cada terminal de cliente**
- Veja as mensagens aparecerem no terminal de logs!

---

## 🧪 Testes de Estresse

### Via Menu (abre em novo terminal)
```bash
./docker-menu.sh
# [5] Teste TCP
# [6] Teste UDP
```

### Manual
```bash
# TCP (5000 clientes, 5 mensagens)
docker compose run --rm teste-estresse-tcp

# UDP (500 clientes, 100 mensagens)
docker compose run --rm teste-estresse-udp

# Personalizado
docker compose run --rm \
  -e TOTAL_CLIENTES=1000 \
  -e MENSAGENS_POR_CLIENTE=10 \
  teste-estresse-tcp
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

## ⚡ Vantagens

- ✅ Cada componente em terminal separado
- ✅ Logs isolados e limpos
- ✅ Controle visual total
- ✅ Fácil de gerenciar múltiplos clientes
- ✅ Não precisa alternar entre terminais manualmente
