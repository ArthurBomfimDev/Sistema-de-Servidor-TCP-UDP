# 📚 Parte Teórica - Protocolos de Rede e Threading

## 1. Diferenças entre TCP e UDP

### 🔵 TCP (Transmission Control Protocol)

#### **Como funciona o three-way handshake**

> É um processo de 3 passos (aperto de mão triplio), que garente uma conexão segura entre o cliente e servidor.

```
1️⃣ SYN      → Cliente envia pacote de sincronização
2️⃣ SYN-ACK  → Servidor confirma e sincroniza de volta
3️⃣ ACK      → Cliente confirma a resposta do servidor
```

- **1) SYN:** O cliente envia um pacote de sincronização. (Perguntando se o sevidor escuta) garantindo a localização do servidor
- **2) SYN-ACK:** O servidor responde confirmando o recebimento e sincronizando de volta. Se o servidor não responder o cliente eniva novamente uma mensagem.
- **3) ACK:** O cliente confirma a resposta do servidor. Apartir disso começa a troca de mensagens

✅ Isso garante que ambos os lados estejam prontos para trocar dados

---

#### **Garantia de entrega e ordem dos pacotes**

O pacote TCP pode ser mais lento se comparado ao UDP, porém ele garante que todos os dados cheguem; se algum pacote se perder, é feito o reenvio automaticamente. Além da confiabilidade, o TCP numera todos os pacotes: se eles chegarem fora de ordem, ele os organiza antes de entregar para a aplicação.

---

#### **Controle de fluxo e congestionamento**

O TCP ajusta a velocidade dos envios para evitar o congestionamento no receptor ou na rede, impedindo que sejam enviados mais pacotes do que o sistema pode processar.

---

#### **Overhead de conexão**

Esse overhead, refere-se ao gasto extra que o protocolo nescessita para funcionar. O Primeiro peso extra, acontece com o TCP three-way handshake, além do cabeçalho que contem informações de controle (quem é o pacto, qual a ordem, etc.) esse cabeçalho tem um custo a mais de 20 bytes, fora que toda mensagem precisa de ack

---

### 🟣 UDP (User Datagram Protocol)

#### **Protocolo sem conexão**

Diferente do TCP, ele não estabelece um "aperto de mão". O emissor simplesmente envia os dados para o destino sem verificar se ele está pronto ou online.

#### **Sem garantia de entrega**

Não há confirmação de recebimento. Se um pacote cair ou se perder no caminho, o protocolo não solicita o reenvio. O que chegou, chegou.

#### **Menor latência**

Por ser direto e não ter as burocracias de checagem do TCP, a transmissão é muito mais rápida, ideal para comunicações em tempo real.

#### **Casos de uso ideais**

Muito utilizado em qualquer tipo de serviço em tempo real que precisa de uma latencia menor, como por exemplo: Transmissões de vídeo (Streaming), chamadas de voz (VoIP) e jogos online, onde a velocidade é mais importante do que a perda ocasional de um pequeno detalhe.

---

## 2. Comportamento no Sistema de Chat

### 📦 O que acontece quando um pacote se perde?

**🔵 TCP:**
O sistema pausa a entrega e reenvia o dado perdido. No chat, a mensagem pode demorar alguns milissegundos a mais para aparecer, mas ela chegará completa e na ordem correta.

**🟣 UDP:**
A mensagem simplesmente fica com um "buraco" ou o pedaço da voz some. Como não há reenvio, o sistema ignora a perda e continua transmitindo o que vem a seguir.

---

### 👥 Como cada protocolo lida com múltiplos clientes?

**🔵 TCP:**
Mantém uma conexão dedicada (Socket) e persistente para cada usuário. O servidor precisa monitorar cada "túnel" individualmente.

**🟣 UDP:**
Trabalha de forma livre, podendo enviar dados para vários endereços ao mesmo tempo sem precisar gerenciar o estado ou a "saúde" de cada conexão individual.

---

### ⏱️ Impacto da latência em cada implementação

**🔵 TCP:**
A latência alta causa o famoso "delay" no texto. Como ele espera o ACK (confirmação) para seguir adiante, o usuário sente que a mensagem demorou para "sair" ou "chegar".

**🟣 UDP:**
Causa falhas perceptíveis em tempo real, como áudio robótico, cortes na voz ou "pulos" em transmissões de vídeo.

---

### 💻 Consumo de recursos (memória, CPU)

**🔵 TCP:**
Consome mais RAM (para guardar buffers de retransmissão) e CPU (para processar cabeçalhos e confirmações). O gasto de banda larga é maior, pois além da mensagem, você está enviando dados de controle e recebendo ACKs constantemente.

**🟣 UDP:**
É muito mais leve. Gasta menos banda por ter um cabeçalho menor e não exigir confirmações. Consome o mínimo de recursos do servidor, permitindo escalar para milhares de usuários com menos hardware.

---

## 3. Threading no Contexto do Chat

### 🧵 Por que threading é necessário?

O threading é necessário para permitir múltiplas conexões simultâneas sem que uma trave a outra. Em um chat, o recebimento e o envio de mensagens precisam acontecer ao mesmo tempo; se rodasse em single thread, o servidor ficaria "preso" em uma única tarefa (ou apenas enviando, ou apenas recebendo), travando o atendimento aos outros usuários e impedindo o tempo real.

---

### ⚙️ Gerenciamento de threads (criação, término, limpeza)

A thread permite que o código lide com várias processo ao mesmo tempo, mas exige um bom gerenciamento:

- **Criação:** Criar threads somente quando necessário (ex: por cliente)
- **Término e Limpeza:** É fundamental encerrar as threads e liberar os recursos (memória e sockets) logo após o uso. Se não houver limpeza, ocorre o acúmulo de "threads zumbis", gerando um gasto desnecessário de memória e podendo derrubar o servidor.

---

### 🔒 Sincronização de threads (se necessário)

É o mecanismo usado para evitar que duas threads tentem alterar o mesmo dado ao mesmo tempo (como a lista de usuários online). Usamos Locks: Travas, a primeira thread a utilizar o recurso pode editar, enquanto a outra espera - Pode causar Overhead ou Deadlock. Isso evita corrupção de dados e inconsistências.

---

### 📬 Modelo de gerenciado de fluxo de mensagens em caso de fila (organização)

O processo de fila é necessário em casos de grande fluxo de mensagens onde o servidor não consegue processar tudo instantaneamente. As mensagens são armazenadas em uma fila (organização sequencial) para serem processadas em ordem, garantindo que o servidor não perca dados e mantenha a cronologia do chat.

---

### ⚠️ Desafios comuns

- **Deadlocks:** Quando duas threads ficam travadas esperando uma pela outra e o sistema para.

- **Race Conditions:** Quando o resultado final depende da "corrida" entre threads, gerando bugs imprevisíveis.

- **Consumo de Memória:** Muitas threads abertas simultaneamente podem esgotar a RAM do servidor rapidamente.

---