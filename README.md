# Sistema de Comunicação Cliente-Servidor TCP/UDP

Sistema de mensageria que implementa comunicação via protocolos TCP e UDP, permitindo múltiplos clientes conectados simultaneamente.

## 📁 Arquivos do Projeto

### `src/servidor/servidor.py`
Servidor principal que gerencia conexões TCP e UDP simultaneamente.

**Funcionalidades:**
- Executa servidores TCP e UDP em threads paralelas
- **TCP**: Aceita múltiplos clientes com autenticação por username
- **UDP**: Recebe mensagens sem conexão persistente
- Timeout de 30 segundos para inatividade (TCP)
- Confirmação ACK para mensagens TCP

**Configuração:**
- Host: `0.0.0.0`
- Porta: `5555`

**Como executar:**
```bash
python -m src.servidor.servidor
```

### `src/models/cliente.py`
Classe modelo que representa um cliente conectado.

**Atributos:**
- `id_usuario`: Identificador único (porta do cliente)
- `username`: Nome de usuário
- `socket`: Objeto socket da conexão
- `endereco`: Tupla com informações do endereço

### `src/cliente/cliente_tcp.py`
Cliente TCP com conexão persistente e bidirecional.

**Funcionalidades:**
- Solicita username ao iniciar
- Mantém conexão persistente com o servidor
- Thread dedicada para receber mensagens
- Desconexão automática por timeout (30s de inatividade)
- Recebe confirmações ACK do servidor

**Como executar:**
```bash
python -m src.cliente.cliente_tcp
```

### `src/cliente/cliente_udp.py`
Cliente UDP para comunicação sem conexão.

**Funcionalidades:**
- Envia mensagens sem estabelecer conexão
- Thread para receber respostas (se houver)
- Sem garantia de entrega
- Sem autenticação ou ACK

**Como executar:**
```bash
python -m src.cliente.cliente_udp
```

### `scripts/painel.sh`
Script bash para gerenciar o sistema via menu interativo (execução local).

**Funcionalidades:**
- Menu interativo em loop contínuo
- Inicia servidor em novo terminal
- Cria múltiplos clientes TCP/UDP simultaneamente (cada um em novo terminal)
- Executa testes de estresse em novo terminal
- Limpa variáveis de ambiente que causam conflitos

**Opções do menu:**
- `[1]` - Servidor Gateway (novo terminal)
- `[2]` - Cliente TCP (quantidade personalizável, novos terminais)
- `[3]` - Cliente UDP (quantidade personalizável, novos terminais)
- `[4]` - Teste de Estresse TCP (novo terminal)
- `[5]` - Teste de Estresse UDP (novo terminal)
- `[0]` - Sair

**Como executar:**
```bash
chmod +x scripts/painel.sh
./scripts/painel.sh
```

### `docker-menu.sh`
Script bash para gerenciar o sistema via Docker.

**Funcionalidades:**
- Menu interativo em loop contínuo
- Gerencia containers Docker
- Abre logs do servidor em novo terminal
- Cria múltiplos clientes TCP/UDP em novos terminais
- Executa testes de estresse em novos terminais
- Remove containers órfãos ao parar

**Opções do menu:**
- `[1]` - Iniciar Servidor (background)
- `[2]` - Ver Logs do Servidor (novo terminal)
- `[3]` - Criar Cliente(s) TCP (quantidade personalizável, novos terminais)
- `[4]` - Criar Cliente(s) UDP (quantidade personalizável, novos terminais)
- `[5]` - Teste de Estresse TCP (novo terminal)
- `[6]` - Teste de Estresse UDP (novo terminal)
- `[7]` - Parar Servidor (remove containers)
- `[0]` - Sair

**Como executar:**
```bash
chmod +x docker-menu.sh
./docker-menu.sh
```

### `run-cliente-tcp.sh`
Script auxiliar para criar cliente TCP via Docker.

**Funcionalidades:**
- Solicita nome do cliente
- Abre cliente TCP em novo terminal
- Conecta à rede Docker do servidor

**Como executar:**
```bash
./run-cliente-tcp.sh NomeDoCliente
```

### `run-cliente-udp.sh`
Script auxiliar para criar cliente UDP via Docker.

**Funcionalidades:**
- Abre cliente UDP em novo terminal
- Conecta à rede Docker do servidor

**Como executar:**
```bash
./run-cliente-udp.sh
```

### `tests/teste_estresse.py`
Script para teste de carga TCP com múltiplos clientes simultâneos.

**Funcionalidades:**
- Simula múltiplos clientes TCP conectando simultaneamente
- Configurável via variável de ambiente
- Aguarda ACK do servidor para cada mensagem
- Exibe estatísticas de desempenho ao final

**Variáveis de ambiente:**
- `ALVO_IP`: IP do servidor (padrão: `127.0.0.1`)
- `ALVO_PORTA`: Porta do servidor (padrão: `5555`)
- `TOTAL_CLIENTES`: Número de clientes (padrão: `5000`)
- `MENSAGENS_POR_CLIENTE`: Mensagens por cliente (padrão: `5`)

**Como executar:**
```bash
python tests/teste_estresse.py
```

### `tests/teste_estresse_udp.py`
Script para teste de carga UDP com múltiplos clientes simultâneos.

**Funcionalidades:**
- Simula múltiplos clientes UDP enviando pacotes simultaneamente
- Configurável via variável de ambiente
- Compressão de mensagens com zlib
- Exibe estatísticas de desempenho ao final

**Variáveis de ambiente:**
- `ALVO_IP`: IP do servidor (padrão: `127.0.0.1`)
- `ALVO_PORTA`: Porta do servidor (padrão: `5555`)
- `TOTAL_CLIENTES`: Número de clientes (padrão: `500`)
- `MENSAGENS_POR_CLIENTE`: Mensagens por cliente (padrão: `100`)

**Como executar:**
```bash
python tests/teste_estresse_udp.py
```

## 🚀 Como Usar

### Opção 1: Usando Docker (Recomendado) 🐳

#### Menu Interativo (Mais Fácil)
```bash
./docker-menu.sh
```

O menu permite:
- Iniciar/parar servidor
- Ver logs em tempo real (novo terminal)
- Criar múltiplos clientes TCP/UDP (novos terminais)
- Executar testes de estresse (novos terminais)

#### Comandos Manuais
```bash
# Subir servidor
docker compose up -d

# Ver logs (novo terminal via menu ou manual)
docker compose logs -f servidor

# Criar clientes (abrem novos terminais)
./run-cliente-tcp.sh Arthur
./run-cliente-tcp.sh Maria
./run-cliente-udp.sh

# Testes de estresse
docker compose run --rm teste-estresse-tcp
docker compose run --rm teste-estresse-udp

# Parar tudo
docker compose down
```

**📖 Documentação completa:** [docs/README-DOCKER.md](docs/README-DOCKER.md)

### Opção 2: Usando o Painel de Controle (Execução Local)

```bash
chmod +x scripts/painel.sh
./scripts/painel.sh
```

O menu permite:
- Iniciar servidor (novo terminal)
- Criar múltiplos clientes TCP (novos terminais)
- Criar múltiplos clientes UDP (novos terminais)
- Executar testes de estresse (novos terminais)

### Opção 3: Execução Manual

1. **Inicie o servidor:**
   ```bash
   python -m src.servidor.servidor
   ```

2. **Conecte clientes TCP** (em terminais separados):
   ```bash
   python -m src.cliente.cliente_tcp
   ```
   Digite seu username e comece a enviar mensagens.

3. **Conecte clientes UDP** (opcional):
   ```bash
   python -m src.cliente.cliente_udp
   ```
   Envie mensagens diretamente sem autenticação.

4. **Execute testes de estresse** (opcional):
   ```bash
   # Teste TCP (5000 clientes, 5 mensagens)
   python tests/teste_estresse.py
   
   # Teste UDP (500 clientes, 100 mensagens)
   python tests/teste_estresse_udp.py
   ```

## 🔄 Diferenças TCP vs UDP

| Característica | TCP | UDP |
|----------------|-----|-----|
| Conexão | Persistente | Sem conexão |
| Autenticação | Username obrigatório | Não possui |
| Confirmação | ACK para cada mensagem | Sem confirmação |
| Timeout | 30 segundos | Não possui |
| Confiabilidade | Garantida | Não garantida |

## 📝 Exemplo de Uso

### Usando Docker Menu

**1. Execute o menu:**
```bash
./docker-menu.sh
```

**2. Escolha [1] - Iniciar Servidor**

**3. Escolha [2] - Ver Logs**
- Abre novo terminal com logs em tempo real

**4. Escolha [3] - Criar Cliente TCP**
- Digite: 2 (para criar 2 clientes)
- Abre 2 novos terminais com clientes conectados

**5. Digite mensagens em cada terminal de cliente**

**Resultado no Terminal de Logs:**
```
[INFO] Servidor TCP iniciando 0.0.0.0:5555
[INFO] Aguardando conexões dos clientes...
[INFO] Servidor UDP iniciando 0.0.0.0:5555
[CONNECT] Cliente Id: 40804, username: Cliente_1 conectado de 172.19.0.2
[MESSAGE] Cliente_1: Olá servidor!
[CONNECT] Cliente Id: 40805, username: Cliente_2 conectado de 172.19.0.3
[MESSAGE] Cliente_2: Tudo bem?
```

## ⚙️ Requisitos

### Docker (Recomendado)
- Docker Engine 20.10+
- Docker Compose 2.0+
- gnome-terminal (para abrir múltiplos terminais automaticamente)

### Execução Local
- Python 3.x
- Bibliotecas padrão: `socket`, `threading`, `typing`, `zlib`, `os`
- Bash (para executar scripts .sh)
- gnome-terminal (para abrir múltiplas janelas)

## 🔒 Observações

- O servidor aceita conexões em `0.0.0.0:5555` (todas as interfaces)
- No Docker, clientes conectam via rede bridge interna
- Clientes TCP inativos por mais de 30 segundos são desconectados automaticamente
- Mensagens UDP não recebem confirmação do servidor
- Múltiplos clientes podem se conectar simultaneamente via TCP
- Todos os scripts abrem automaticamente novos terminais para cada componente
- Os menus funcionam em loop contínuo até escolher sair

## 📦 Arquivos Docker

- `Dockerfile` - Imagem base Python 3.11 slim
- `docker-compose.yml` - Orquestração de serviços
- `.dockerignore` - Arquivos excluídos do build
- `docker-menu.sh` - Menu interativo Docker (loop contínuo, novos terminais)
- `run-cliente-tcp.sh` - Script auxiliar cliente TCP (novo terminal)
- `run-cliente-udp.sh` - Script auxiliar cliente UDP (novo terminal)

## 📚 Documentação Adicional

- **[docs/README-DOCKER.md](docs/README-DOCKER.md)** - Guia completo Docker com troubleshooting
- **[docs/GUIA-RAPIDO.md](docs/GUIA-RAPIDO.md)** - Comandos rápidos e exemplos práticos
