# 🐳 Estrutura Docker do Projeto

Este projeto foi totalmente conteinerizado visando **isolamento**, **facilidade de execução** e **simulação de um ambiente de rede real**. A arquitetura utiliza um **Dockerfile** otimizado para a imagem base e o **Docker Compose** para orquestração dos serviços e testes.

---

## 🏗️ Arquitetura das Imagens (Dockerfile)

A imagem do projeto foi construída com foco em **performance** e **leveza**:

- **Imagem Base:** `python:3.12-slim` - Garante um ambiente atualizado com o mínimo de dependências do SO, reduzindo o tamanho do container
- **Logs em Tempo Real:** Utilização da variável `ENV PYTHONUNBUFFERED=1` para impedir que o Python retenha os logs em memória, permitindo o monitoramento instantâneo via terminal
- **Padronização:** Todo o código é isolado no diretório de trabalho `/servidor`

```dockerfile
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /servidor
COPY . .
EXPOSE 5555
```

---

## ⚙️ Orquestração (docker-compose.yml)

O sistema utiliza uma **rede do tipo bridge** (`rede-comunicacao`) isolada da máquina host. O Compose está dividido em serviços lógicos.

### 📦 Serviços Disponíveis

#### 1. **`servidor`** - Gateway Principal
- Expõe as portas TCP e UDP (5555)
- Política de reinício automático (`restart: unless-stopped`)
- Aceita conexões de qualquer origem na rede bridge

#### 2. **`cliente`** - Container Base Interativo
- Preparado para rodar clientes interativos (`cliente_tcp.py` ou `cliente_udp.py`)
- Comunicação direta pelo nome do serviço na rede interna
- Suporte a entrada de terminal (`stdin_open` e `tty`)

#### 3. **`teste-estresse-tcp`** e **`teste-estresse-udp`**
- Containers efêmeros para validar resiliência do sistema
- Aguardam automaticamente a inicialização do servidor via `depends_on`
- Configurados com variáveis de ambiente para conectar ao servidor

---

## 🚀 Como Executar com Docker

### 📋 Pré-requisitos
- Docker Engine 20.10+
- Docker Compose 2.0+

### 1️⃣ Iniciar o Servidor

Para subir apenas o servidor em **background** (modo detached):
```bash
docker compose up -d servidor
```

Para acompanhar os logs em **tempo real**:
```bash
docker compose logs -f servidor
```

### 2️⃣ Executar Clientes Interativos

Para interagir com o servidor manualmente, crie containers efêmeros (que se destroem ao fechar com a flag `--rm`):

**Cliente TCP:**
```bash
docker compose run --rm cliente python cliente_tcp.py
```

**Cliente UDP:**
```bash
docker compose run --rm cliente python cliente_udp.py
```

**Ou use os scripts auxiliares:**
```bash
# Cliente TCP com nome personalizado
./run-cliente-tcp.sh Arthur

# Cliente UDP
./run-cliente-udp.sh
```

### 3️⃣ Executar Testes de Estresse

#### Teste TCP
```bash
docker compose run --rm teste-estresse-tcp
```
O teste usará automaticamente `servidor:5555` como alvo.
Você será solicitado a informar:
- Número de clientes simultâneos (padrão: `100`)
- Mensagens por cliente (padrão: `5`)

#### Teste UDP
```bash
docker compose run --rm teste-estresse-udp
```
O teste usará automaticamente `servidor:5555` como alvo.
Você será solicitado a informar:
- Número de clientes simultâneos (padrão: `100`)
- Mensagens por cliente (padrão: `10`)

### 4️⃣ Encerrar o Ambiente

Para derrubar os containers e a rede virtual do projeto:
```bash
docker compose down
```

Para remover também os volumes:
```bash
docker compose down -v
```

---

## 🎯 Menu Interativo

Para facilitar o uso, utilize o menu interativo:
```bash
./docker-menu.sh
```

**Opções disponíveis:**
- `[1]` Iniciar Servidor
- `[2]` Ver Logs do Servidor
- `[3]` Criar Cliente TCP
- `[4]` Criar Cliente UDP
- `[5]` Teste de Estresse TCP
- `[6]` Teste de Estresse UDP
- `[7]` Parar Servidor
- `[0]` Sair

---

## ⛔️ Variáveis de Ambiente

### Servidor
Não requer variáveis de ambiente. Configurado para:
- `HOST`: `0.0.0.0` (aceita conexões de qualquer origem na rede Docker)
- `PORTA`: `5555`

### Clientes (cliente_tcp.py e cliente_udp.py)
- `ALVO_IP`: Endereço do servidor (padrão: `servidor` no Docker, `127.0.0.1` local)
- `ALVO_PORTA`: Porta (padrão: `5555`)

### Testes de Estresse
- `ALVO_IP`: Endereço do servidor (padrão: `127.0.0.1`, no Docker: `servidor`)
- `ALVO_PORTA`: Porta (padrão: `5555`)
- Número de clientes e mensagens são solicitados via input durante a execução

---

## 📊 Exemplo Completo de Uso

### Terminal 1: Servidor
```bash
docker compose up servidor
```
**Saída:**
```
[INFO] Servidor TCP iniciando 0.0.0.0:5555
[INFO] Aguardando conexões dos clientes...
[INFO] Servidor UDP iniciando 0.0.0.0:5555
```

### Terminal 2: Cliente TCP 1
```bash
./run-cliente-tcp.sh Arthur
```
```
Digite seu nome de usuario: Arthur
Conectado ao servidor!
> Olá servidor!
[MESSAGE] ACK - ID: 40804
```

### Terminal 3: Cliente TCP 2
```bash
./run-cliente-tcp.sh Maria
```
```
Digite seu nome de usuario: Maria
Conectado ao servidor!
> Oi pessoal!
[MESSAGE] ACK - ID: 40805
```

### Terminal 4: Cliente UDP
```bash
./run-cliente-udp.sh
```
```
> Mensagem UDP de teste
```

### Terminal 5: Teste de Estresse
```bash
docker compose run --rm teste-estresse-tcp
# Input Clientes: 100
# Input Mensagens: 5
```
**Saída:**
```
============================================================
  TESTE DE ESTRESSE TCP
============================================================
Alvo: servidor:5555
============================================================
Número de clientes simultâneos (padrão 100): 100
Mensagens por cliente (padrão 5): 5

Alvo: servidor:5555
Clientes: 100
Mensagens por cliente: 5
Total de mensagens: 500
============================================================

[FINALIZADO] Bot_0 concluiu as tarefas.
[FINALIZADO] Bot_1 concluiu as tarefas.
...
============================================================
  TESTE CONCLUÍDO COM SUCESSO
============================================================
```

---

## 🔍 Comandos Úteis

### Monitoramento
```bash
# Status dos containers
docker compose ps

# Estatísticas de recursos (CPU, memória, rede)
docker stats

# Logs específicos (últimas 50 linhas)
docker compose logs --tail=50 servidor

# Logs em tempo real
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

# Limpar tudo (containers, redes, volumes)
docker compose down -v
docker system prune -f
```

### Debug de Rede
```bash
# Inspecionar rede
docker network inspect desafio-sistema-servidor-tcp-udp_rede-comunicacao

# Testar conectividade
docker run --rm --network desafio-sistema-servidor-tcp-udp_rede-comunicacao \
  busybox ping servidor
```

---

## 🐛 Troubleshooting

### Porta 5555 em uso
```bash
# Verificar processos usando a porta
sudo lsof -i :5555

# Ou mudar porta no docker-compose.yml
ports:
  - "5556:5555/tcp"
  - "5556:5555/udp"
```

### Cliente não conecta
```bash
# Verificar se servidor está rodando
docker compose ps servidor

# Ver logs de erro
docker compose logs servidor

# Testar conectividade na rede
docker run --rm --network desafio-sistema-servidor-tcp-udp_rede-comunicacao \
  busybox telnet servidor 5555
```

### Reconstruir ambiente do zero
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d servidor
```

---

## 🏛️ Arquitetura de Rede

```
┌─────────────────────────────────────────────┐
│     rede-comunicacao (bridge - isolada)     │
│                                             │
│         ┌──────────────────────┐            │
│         │   Servidor Gateway   │            │
│         │   TCP + UDP :5555    │            │
│         │  (servidor-tcp-udp)  │            │
│         └─────────┬────────────┘            │
│                   │                         │
│     ┌────────┬────┼───┬──────────┐          │
│     │        │        │          │          │
│  ┌──▼───┐ ┌─▼────┐ ┌─▼────┐ ┌──▼──────┐     │
│  │TCP-1 │ │TCP-2 │ │UDP-1 │ │ Stress  │     │
│  │Arthur│ │Maria │ │      │ │ Test    │     │
│  └──────┘ └──────┘ └──────┘ └─────────┘     │
└─────────────────────────────────────────────┘
         │
         │ Porta 5555 (TCP/UDP)
         ▼
    [Host Machine]
```

---

## 🔐 Segurança

- ✅ Containers em rede isolada (bridge)
- ✅ Apenas porta 5555 exposta ao host
- ✅ Sem privilégios elevados
- ✅ Imagem base oficial Python slim
- ✅ Sem credenciais hardcoded

---

## 📦 Estrutura de Arquivos Docker

```
.
├── docker-compose.yml      # Orquestração de serviços
├── dockerfile              # Imagem base da aplicação
├── .dockerignore          # Arquivos excluídos do build
├── docker-menu.sh         # Menu interativo
├── run-cliente-tcp.sh     # Script auxiliar TCP
├── run-cliente-udp.sh     # Script auxiliar UDP
├── teste_estresse.py      # Teste de carga TCP
└── teste_estresse_udp.py  # Teste de carga UDP
```

---

## ✅ Vantagens da Abordagem Docker

- ✅ **Isolamento completo** - Cada componente em seu próprio container
- ✅ **Reprodutibilidade** - Mesmo ambiente em qualquer máquina
- ✅ **Escalabilidade** - Fácil criar múltiplos clientes
- ✅ **Logs limpos** - Separação clara entre servidor e clientes
- ✅ **Rede simulada** - Ambiente próximo ao real
- ✅ **Testes automatizados** - Validação de resiliência simplificada
- ✅ **Zero configuração** - Funciona out-of-the-box

---

## 🎓 Conceitos Técnicos Aplicados

### Por que o servidor inicia automaticamente ao rodar os testes?

Isso acontece por causa do **`depends_on`** no Docker Compose:

- No `docker-compose.yml`, os testes de estresse têm `depends_on: - servidor`
- Quando você executa `docker compose run teste-estresse-tcp`, o Docker verifica as dependências
- Como o teste depende do servidor, o Docker garante que o servidor esteja rodando primeiro
- Se o servidor não estiver ativo, ele será iniciado automaticamente
- Quando você não usa a flag `-d`, os logs de ambos os containers aparecem no terminal

---

## 📚 Referências

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Networking](https://docs.docker.com/network/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
