# 🐳 Docker - Sistema Cliente-Servidor TCP/UDP

## 📋 Pré-requisitos

- Docker Engine 20.10+
- Docker Compose 2.0+
- gnome-terminal (para abrir terminais automaticamente)

## 🚀 Início Rápido

### Menu Interativo (RECOMENDADO)
```bash
./docker-menu.sh
```

Todas as opções abrem automaticamente em novos terminais!

### Passo a Passo Manual

#### 1. Iniciar Servidor
```bash
docker compose up -d
```

#### 2. Ver Logs (novo terminal)
```bash
./docker-menu.sh
# Opção [2]
```

#### 3. Criar Clientes TCP (cada um em novo terminal)
```bash
./run-cliente-tcp.sh Arthur
./run-cliente-tcp.sh Maria
./run-cliente-tcp.sh João
```

#### 4. Criar Cliente UDP (novo terminal)
```bash
./run-cliente-udp.sh
```

#### 5. Parar
```bash
docker compose down
```

---

## 🎯 Uso Detalhado

### Menu Interativo

Execute o menu:
```bash
./docker-menu.sh
```

**Opções disponíveis:**
- **[1] Iniciar Servidor** - Inicia o servidor em background
- **[2] Ver Logs do Servidor** - Abre logs em novo terminal
- **[3] Criar Cliente TCP** - Solicita nome e abre cliente em novo terminal
- **[4] Criar Cliente UDP** - Abre cliente UDP em novo terminal
- **[5] Teste de Estresse TCP** - Executa teste em novo terminal
- **[6] Teste de Estresse UDP** - Executa teste em novo terminal
- **[7] Parar Servidor** - Para e remove containers
- **[0] Sair** - Fecha o menu

### Fluxo de Trabalho Recomendado

1. Execute `./docker-menu.sh` e escolha **[1]** para iniciar servidor
2. Execute `./docker-menu.sh` novamente e escolha **[2]** para ver logs
3. Execute `./docker-menu.sh` novamente e escolha **[3]** para criar cliente TCP
4. Repita o passo 3 para criar mais clientes
5. Digite mensagens em cada terminal de cliente
6. Observe as mensagens no terminal de logs

---

## 🧪 Testes de Estresse

### Via Menu (novo terminal)
```bash
./docker-menu.sh
# [5] para TCP
# [6] para UDP
```

O menu solicitará:
- Número de clientes (padrão: 5000 TCP / 500 UDP)
- Mensagens por cliente (padrão: 5 TCP / 100 UDP)

### Manual

#### TCP (5000 clientes, 5 mensagens)
```bash
docker compose run --rm teste-estresse-tcp
```

#### UDP (500 clientes, 100 mensagens)
```bash
docker compose run --rm teste-estresse-udp
```

#### Personalizado
```bash
# TCP com 1000 clientes e 10 mensagens
docker compose run --rm \
  -e TOTAL_CLIENTES=1000 \
  -e MENSAGENS_POR_CLIENTE=10 \
  teste-estresse-tcp

# UDP com 200 clientes e 50 mensagens
docker compose run --rm \
  -e TOTAL_CLIENTES=200 \
  -e MENSAGENS_POR_CLIENTE=50 \
  teste-estresse-udp
```

---

## 🔧 Comandos Úteis

### Monitoramento
```bash
# Status dos containers
docker compose ps

# Estatísticas de recursos
docker stats

# Logs manuais (sem novo terminal)
docker compose logs -f servidor
```

### Manutenção
```bash
# Reiniciar servidor
docker compose restart servidor

# Reconstruir imagens
docker compose build

# Rebuild sem cache
docker compose build --no-cache

# Limpar tudo
docker compose down -v
docker system prune -f
```

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────┐
│    rede-comunicacao (bridge)    │
│                                 │
│  ┌──────────────┐               │
│  │   Servidor   │ :5555         │
│  │  TCP + UDP   │               │
│  └──────┬───────┘               │
│         │                        │
│    ┌────┴────┬────────┐         │
│    │         │        │         │
│ ┌──▼───┐ ┌──▼───┐ ┌──▼───┐    │
│ │TCP-1 │ │TCP-2 │ │UDP-1 │    │
│ └──────┘ └──────┘ └──────┘    │
└─────────────────────────────────┘

Cada componente em terminal separado!
```

---

## ⚙️ Variáveis de Ambiente

### Servidor
- `HOST`: IP de bind (padrão: `0.0.0.0`)
- `PORTA`: Porta (padrão: `5555`)

### Clientes
- `HOST`: Endereço do servidor (padrão: `servidor`)
- `PORT`: Porta (padrão: `5555`)

### Testes de Estresse
- `ALVO_IP`: IP do servidor (padrão: `servidor`)
- `ALVO_PORTA`: Porta (padrão: `5555`)
- `TOTAL_CLIENTES`: Número de clientes
- `MENSAGENS_POR_CLIENTE`: Mensagens por cliente

---

## 🐛 Troubleshooting

### Porta 5555 em uso
```bash
# Verificar
sudo lsof -i :5555

# Ou mudar porta no docker-compose.yml
ports:
  - "5556:5555"
```

### Cliente não conecta
```bash
# Verificar servidor
docker compose ps servidor

# Ver logs
docker compose logs servidor

# Reconstruir
docker compose down -v
docker compose build
docker compose up -d
```

### gnome-terminal não encontrado
```bash
# Instalar no Ubuntu/Debian
sudo apt install gnome-terminal

# Ou edite os scripts para usar outro terminal:
# xterm, konsole, xfce4-terminal, etc.
```

---

## 📊 Exemplo Completo

### 1. Inicie o menu
```bash
./docker-menu.sh
```

### 2. Escolha [1] - Iniciar Servidor
```
✓ Servidor iniciado!
```

### 3. Execute menu novamente e escolha [2] - Ver Logs
```
Novo terminal abre com:
[INFO] Servidor TCP iniciando 0.0.0.0:5555
[INFO] Servidor UDP iniciando 0.0.0.0:5555
```

### 4. Execute menu novamente e escolha [3] - Cliente TCP
```
Nome do cliente TCP: Arthur
✓ Cliente TCP aberto em novo terminal
```

### 5. Execute menu novamente e escolha [3] - Cliente TCP
```
Nome do cliente TCP: Maria
✓ Cliente TCP aberto em novo terminal
```

### 6. Digite mensagens nos terminais dos clientes

**Terminal Cliente Arthur:**
```
Digite seu nome de usuario: Conectado ao servidor!
Olá servidor!
[MESSAGE] ACK - ID: 12345
```

**Terminal Cliente Maria:**
```
Digite seu nome de usuario: Conectado ao servidor!
Tudo bem?
[MESSAGE] ACK - ID: 12346
```

**Terminal Logs:**
```
[CONNECT] Cliente Id: 12345, username: Arthur conectado de 172.19.0.2
[MESSAGE] Arthur: Olá servidor!
[CONNECT] Cliente Id: 12346, username: Maria conectado de 172.19.0.3
[MESSAGE] Maria: Tudo bem?
```

---

## 🔐 Segurança

- Containers em rede isolada (bridge)
- Apenas porta 5555 exposta ao host
- Sem privilégios elevados
- Imagem base oficial Python slim

---

## 📦 Estrutura de Arquivos

```
.
├── docker-compose.yml      # Orquestração
├── Dockerfile             # Imagem base
├── .dockerignore          # Exclusões do build
├── docker-menu.sh         # Menu interativo (abre novos terminais)
├── run-cliente-tcp.sh     # Script cliente TCP (novo terminal)
├── run-cliente-udp.sh     # Script cliente UDP (novo terminal)
├── servidor.py            # Servidor
├── cliente_tcp.py         # Cliente TCP
├── cliente_udp.py         # Cliente UDP
├── teste_estresse.py      # Teste TCP
└── teste_estresse_udp.py  # Teste UDP
```

---

## ✅ Vantagens desta Configuração

- ✅ Cada componente em terminal separado automaticamente
- ✅ Logs isolados e limpos
- ✅ Controle visual total do sistema
- ✅ Fácil gerenciar múltiplos clientes
- ✅ Não precisa alternar entre terminais manualmente
- ✅ Interface amigável via menu
- ✅ Testes de estresse configuráveis
