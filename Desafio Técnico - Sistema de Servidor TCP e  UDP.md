# Desafio Técnico - Sistema de Servidor com TCP e UDP

## Objetivo
Desenvolver um sistema de Servidor em Python que demonstre as diferenças práticas entre protocolos TCP e UDP, utilizando threading para suportar múltiplas conexões simultâneas.

---

## Descrição do Desafio

Você deve criar **um servidores de chat**: um usando TCP e outro usando UDP. Os servidores devem permitir que múltiplos clientes se conectem e troquem mensagens entre si. A implementação deve destacar as características de cada protocolo, como confiabilidade e ordem de entrega.

### Requisitos Funcionais

#### Parte 1: Servidor TCP
- Aceitar múltiplas conexões de clientes simultaneamente
- Cada cliente deve ter um identificador único (nickname/id_user)
- Transmitir mensagens do cliente para o server e vice-versa
- Gerenciar entrada e saída de clientes do chat
- Usar threading para lidar com cada cliente 
- Manter registro dos clientes ativos (endereço IP e porta)

#### Parte 2: Servidor UDP
- Receber mensagens de múltiplos clientes
- Usar threading para escutar e enviar mensagens

#### Parte 3: Clientes
- Criar clientes para TCP e UDP
- Permitir envio e recebimento simultâneo de mensagens
- Interface simples via terminal
---

## Especificações Técnicas

### Servidor TCP (porta: localhost)
```python
# Funcionalidades esperadas:
- socket.socket(socket.AF_INET, socket.SOCK_STREAM)
- threading.Thread para cada cliente
- Tratamento de exceções para desconexões
```

### Servidor UDP (porta: localhost)
```python
# Funcionalidades esperadas:
- socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
- Dicionário para rastrear clientes ativos
- Sistema de timeout para remover clientes inativos
- Thread separada para verificação de keep-alive
```

---

## Estrutura de Arquivos Sugerida

```
chat_system/
│
├── tcp_server.py          # Servidor TCP
├── tcp_client.py          # Cliente TCP
├── udp_server.py          # Servidor UDP
├── udp_client.py          # Cliente UDP
├── requirements.txt       # Dependências (se houver)
└── README.md             # Sua documentação
```

---

## Parte Teórica (OBRIGATÓRIA)

Você deve criar um documento explicando:

### 1. Diferenças entre TCP e UDP

**TCP (Transmission Control Protocol)**
- Como funciona o three-way handshake
- Garantia de entrega e ordem dos pacotes
- Controle de fluxo e congestionamento
- Overhead de conexão

**UDP (User Datagram Protocol)**
- Protocolo sem conexão
- Sem garantia de entrega
- Menor latência
- Casos de uso ideais

### 2. Comportamento no Sistema de Chat

Compare e descreva:
- O que acontece quando um pacote se perde?
- Como cada protocolo lida com múltiplos clientes?
- Impacto da latência em cada implementação
- Consumo de recursos (memória, CPU)

### 3. Threading no Contexto do Chat

Explique:
- Por que threading é necessário?
- Gerenciamento de threads (criação, término, limpeza)
- Sincronização de threads (se necessário)
- Modelo de gerenciado de fluxo de mensagens em caso de fila (organização)
- Desafios comuns
---

## Desafios Extras (Opcionais)

Para destacar-se, você pode implementar:

1. **Compressão**: Implementar compressão de dados no UDP
2. **Protocolo híbrido**: Combinar TCP (controle) e UDP (mensagens)
3. **Testes de stress**: Script para conectar múltiplos clientes simultaneamente
4. **Reconexão automática**: Cliente tenta reconectar em caso de falha
5. **Mensagens de sistema**: Notificações quando usuários entram/saem
6. **Docker**: Usar Docker / Docker-Compose

---

## Exemplos de Uso Esperados

### Servidor TCP
```bash
$ python tcp_server.pyteste
[INFO] Servidor TCP iniciado na porta 5000
[INFO] Aguardando conexões...
[CONNECT] Cliente 123456789 conectado de 127.0.0.1:52341
[CONNECT] Cliente 987654321 conectado de 127.0.0.1:52342
[MESSAGE] 123456789 : "24780116320913362905022621466880060480996862000045fffffbffff00117800007c0902d40400000006009468"
[MESSAGE] 987654321 : "24917105616916483403022626550994000564815002023049fbfffdff005b9d0f0000000000000000000000a3"
[DISCONNECT] Cliente 123456789 desconectado
```

### Cliente TCP
```bash
$ python tcp_client.py
Cliente: 123456789
Conectado ao servidor!
123456789 : "ACK"
```

### Servidor UDP
```bash
$ python udp_server.py
[INFO] Servidor UDP iniciado na porta 5001
[INFO] Aguardando mensagens...
[REGISTER] Novo cliente 123456789 registrado de 127.0.0.1:54123
[MESSAGE] 123456789 : "24780116320913362905022621466880060480996862000045fffffbffff00117800007c0902d40400000006009468"
```

---

## Entrega

**Formato**: Repositório Git (GitHub/GitLab)

**Deve conter**:
- Código-fonte completo e funcional
- README.md com instruções de execução
- Documento teórico (PDF ou Markdown)

**Apresentação:** 12/02/2026

---
## Recursos de Apoio

### Documentação Oficial
- [Python socket](https://docs.python.org/3/library/socket.html)
- [Python threading](https://docs.python.org/3/library/threading.html)

### Tutoriais Recomendados
- Real Python - [Socket Programming](https://realpython.com/python-sockets/)
- GeeksforGeeks - [TCP vs UDP](https://www.geeksforgeeks.org/differences-between-tcp-and-udp/)
- Python Network Programming Cookbook - [E-book](https://github.com/ManhNho/Python-Books-for-Security/blob/master/Python-Network-Programming-Cookbook.pdf) 

---

## Dicas Importantes

⚠️ **Atenção**: 
- Use `try-except` para capturar erros de rede

🐛 **Debug**: 
- Use `print()` estrategicamente para rastrear o fluxo de mensagens
- Teste com `localhost` (0.0.0.0) antes de usar em rede

---

## Checklist Final

Antes de entregar, verifique:

- [ ] Código está comentado e organizado
- [ ] README.md contém instruções claras de execução
- [ ] Ambos servidores (TCP e UDP) funcionam
- [ ] Múltiplos clientes podem se conectar
- [ ] Tratamento de erros implementado
- [ ] Documento teórico completo
- [ ] Testes realizados e documentados
- [ ] Código segue PEP 8 (use `pylint` ou `flake8`)
- [ ] Repositório Git com histórico de commits

---
