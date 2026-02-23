# Sistema de Comunicação Cliente-Servidor TCP/UDP

Sistema de mensageria que implementa comunicação via protocolos TCP e UDP, permitindo múltiplos clientes conectados simultaneamente.

## 📁 Arquivos do Projeto

### `servidor.py`
Servidor principal que gerencia conexões TCP e UDP simultaneamente.

**Funcionalidades:**
- Executa servidores TCP e UDP em threads paralelas
- **TCP**: Aceita múltiplos clientes com autenticação por username
- **UDP**: Recebe mensagens sem conexão persistente
- Timeout de 30 segundos para inatividade (TCP)
- Confirmação ACK para mensagens TCP

**Configuração:**
- Host: `127.0.0.1` (localhost)
- Porta: `5555`

**Como executar:**
```bash
python servidor.py
```

### `cliente.py`
Classe modelo que representa um cliente conectado.

**Atributos:**
- `id_usuario`: Identificador único (porta do cliente)
- `username`: Nome de usuário
- `socket`: Objeto socket da conexão
- `endereco`: Tupla com informações do endereço

### `cliente_tcp.py`
Cliente TCP com conexão persistente e bidirecional.

**Funcionalidades:**
- Solicita username ao iniciar
- Mantém conexão persistente com o servidor
- Thread dedicada para receber mensagens
- Desconexão automática por timeout (30s de inatividade)
- Recebe confirmações ACK do servidor

**Como executar:**
```bash
python cliente_tcp.py
```

### `cliente_udp.py`
Cliente UDP para comunicação sem conexão.

**Funcionalidades:**
- Envia mensagens sem estabelecer conexão
- Thread para receber respostas (se houver)
- Sem garantia de entrega
- Sem autenticação ou ACK

**Como executar:**
```bash
python cliente_udp.py
```

### `painel.sh`
Script bash para gerenciar o sistema via menu interativo (execução local).

**Funcionalidades:**
- Menu interativo para iniciar componentes
- Inicia servidor em terminal separado
- Permite criar múltiplos clientes TCP/UDP simultaneamente
- Permite executar testes de estresse TCP/UDP
- Abre cada instância em nova janela do gnome-terminal

**Opções do menu:**
- `[1]` - Iniciar Servidor Gateway
- `[2]` - Criar clientes TCP (quantidade personalizável)
- `[3]` - Criar clientes UDP (quantidade personalizável)
- `[4]` - Executar teste de estresse TCP
- `[5]` - Executar teste de estresse UDP
- `[0]` - Sair

**Como executar:**
```bash
chmod +x painel.sh
./painel.sh
```

### `docker-menu.sh`
Script bash para gerenciar o sistema via Docker.

**Funcionalidades:**
- Menu interativo para gerenciar containers Docker
- Inicia/para servidor
- Cria clientes TCP/UDP em containers
- Executa testes de estresse
- Visualiza logs do servidor

**Opções do menu:**
- `[1]` - Iniciar Servidor
- `[2]` - Ver Logs do Servidor
- `[3]` - Criar Cliente TCP
- `[4]` - Criar Cliente UDP
- `[5]` - Teste de Estresse TCP
- `[6]` - Teste de Estresse UDP
- `[7]` - Parar Servidor
- `[0]` - Sair

**Como executar:**
```bash
chmod +x docker-menu.sh
./docker-menu.sh
```

### `teste_estresse.py`
Script para teste de carga TCP com múltiplos clientes simultâneos.

**Funcionalidades:**
- Simula múltiplos clientes TCP conectando simultaneamente
- Configurável via variável de ambiente (IP e porta) e input (clientes e mensagens)
- Aguarda ACK do servidor para cada mensagem
- Exibe estatísticas de desempenho ao final

**Variáveis de ambiente:**
- `ALVO_IP`: IP do servidor (padrão: `127.0.0.1`)
- `ALVO_PORTA`: Porta do servidor (padrão: `5555`)

**Como executar:**
```bash
python teste_estresse.py
# Informe: clientes (100), mensagens (5)
```

### `teste_estresse_udp.py`
Script para teste de carga UDP com múltiplos clientes simultâneos.

**Funcionalidades:**
- Simula múltiplos clientes UDP enviando pacotes simultaneamente
- Configurável via variável de ambiente (IP e porta) e input (clientes e mensagens)
- Compressão de mensagens com zlib
- Exibe estatísticas de desempenho ao final

**Variáveis de ambiente:**
- `ALVO_IP`: IP do servidor (padrão: `127.0.0.1`)
- `ALVO_PORTA`: Porta do servidor (padrão: `5555`)

**Como executar:**
```bash
python teste_estresse_udp.py
# Informe: clientes (100), mensagens (10)
```

## 🚀 Como Usar

<<<<<<< Updated upstream
### Opção 1: Usando o Painel de Controle (Recomendado)
=======
### Opção 1: Usando Docker (Recomendado) 🐳

```bash
# Subir servidor
docker compose up -d servidor

# Ver logs
docker compose logs -f servidor

# Executar teste de estresse TCP
docker compose run --rm teste-estresse-tcp

# Executar teste de estresse UDP
docker compose run --rm teste-estresse-udp

# Parar tudo
docker compose down
```

**📖 Documentação completa:** [README-DOCKER.md](README-DOCKER.md)

### Opção 2: Usando o Painel de Controle (Execução Local)
>>>>>>> Stashed changes
```bash
chmod +x painel.sh
./painel.sh
```
Selecione as opções do menu para iniciar servidor, clientes e testes de estresse.

<<<<<<< Updated upstream
### Opção 2: Execução Manual
=======
### Opção 3: Usando o Menu Docker
```bash
chmod +x docker-menu.sh
./docker-menu.sh
```
Gerencia containers Docker via menu interativo.

### Opção 4: Execução Manual
>>>>>>> Stashed changes

1. **Inicie o servidor:**
   ```bash
   python servidor.py
   ```

2. **Conecte clientes TCP** (em terminais separados):
   ```bash
   python cliente_tcp.py
   ```
   Digite seu username e comece a enviar mensagens.

3. **Conecte clientes UDP** (opcional):
   ```bash
   python cliente_udp.py
   ```
   Envie mensagens diretamente sem autenticação.

4. **Execute testes de estresse** (opcional):
   ```bash
   # Teste TCP (usa 127.0.0.1:5555 por padrão)
   python teste_estresse.py
   # Informe: clientes (100), mensagens (5)
   
   # Teste UDP (usa 127.0.0.1:5555 por padrão)
   python teste_estresse_udp.py
   # Informe: clientes (100), mensagens (10)
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

**Terminal 1 - Servidor:**
```
[INFO] Servidor TCP iniciando 127.0.0.1:5555
[INFO] Aguardando conexões dos clientes...
[INFO] Servidor UDP iniciando 127.0.0.1:5555
[CONNECT] Cliente Id: 54321, username: Arthur conectado de 127.0.0.1
[MESSAGE] Arthur: Olá servidor!
```

**Terminal 2 - Cliente TCP:**
```
Digite seu nome de usuario: Arthur
Conectado ao servidor!
Olá servidor!
[MESSAGE] ACK - ID: 54321
```

## ⚙️ Requisitos

- Python 3.x
- Bibliotecas padrão: `socket`, `threading`, `typing`
- Bash (para executar painel.sh)
- gnome-terminal (para abrir múltiplas janelas via painel)

## 🔒 Observações

- O servidor aceita conexões apenas em localhost (127.0.0.1)
- Clientes TCP inativos por mais de 30 segundos são desconectados automaticamente
- Mensagens UDP não recebem confirmação do servidor
- Múltiplos clientes podem se conectar simultaneamente via TCP
