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
Script bash para gerenciar o sistema via menu interativo.

**Funcionalidades:**
- Menu interativo para iniciar componentes
- Inicia servidor em terminal separado
- Permite criar múltiplos clientes TCP/UDP simultaneamente
- Abre cada instância em nova janela do gnome-terminal

**Opções do menu:**
- `[1]` - Iniciar Servidor Gateway
- `[2]` - Criar clientes TCP (quantidade personalizável)
- `[3]` - Criar clientes UDP (quantidade personalizável)
- `[0]` - Sair

**Como executar:**
```bash
chmod +x painel.sh
./painel.sh
```

## 🚀 Como Usar

### Opção 1: Usando Docker (Recomendado) 🐳

```bash
# Subir servidor e clientes
docker-compose up -d

# Ver logs
docker-compose logs -f

# Executar teste de estresse TCP
docker-compose --profile stress-test run --rm teste-estresse-tcp

# Executar teste de estresse UDP
docker-compose --profile stress-test run --rm teste-estresse-udp

# Parar tudo
docker-compose down
```

**📖 Documentação completa:** [README-DOCKER.md](README-DOCKER.md)

### Opção 2: Usando o Painel de Controle
```bash
chmod +x painel.sh
./painel.sh
```
Selecione as opções do menu para iniciar servidor e clientes automaticamente.

### Opção 3: Execução Manual

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

### Docker (Recomendado)
- Docker Engine 20.10+
- Docker Compose 2.0+

### Execução Local
- Python 3.x
- Bibliotecas padrão: `socket`, `threading`, `typing`, `zlib`
- Bash (para executar painel.sh)
- gnome-terminal (para abrir múltiplas janelas via painel)

## 🔒 Observações

- O servidor aceita conexões apenas em localhost (127.0.0.1) quando executado localmente
- No Docker, o servidor aceita conexões de qualquer origem na rede bridge
- Clientes TCP inativos por mais de 30 segundos são desconectados automaticamente
- Mensagens UDP não recebem confirmação do servidor
- Múltiplos clientes podem se conectar simultaneamente via TCP

## 📦 Arquivos Docker

- `Dockerfile` - Imagem base da aplicação
- `docker-compose.yml` - Orquestração de serviços
- `.dockerignore` - Arquivos excluídos do build
- `README-DOCKER.md` - Documentação completa do Docker
