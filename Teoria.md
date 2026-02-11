1. Diferenças entre TCP e UDP
TCP (Transmission Control Protocol)

Como funciona o three-way handshake
É um processo de 3 passos (aperto de mão triplio), que garente uma conexão segura entre o cliente e servidor.  O primeiro passo o cliente envia uma mensagem (perguntando se o sevidor escuta), garantindo 

Garantia de entrega e ordem dos pacotes
O Pacote TCP pode ser mais lento se comparado ao UDP, porém ele garante que todos os dados cheguem, se algum pacote se perder é feito o reenvio. Além da confiabilidade, o TCP, númera todos os pacotes se eles chegarem fora de ordem, ele os organiza antes de chegar na aplicação.

Controle de fluxo e congestionamento
O TCP, ajusta a velocidade dos envios para evitar o congestinamento no receptor ou na rede (mais pacotes do que pode ser processado)

Overhead de conexão
UDP (User Datagram Protocol)

Protocolo sem conexão
Sem garantia de entrega
Menor latência
Casos de uso ideais
2. Comportamento no Sistema de Chat
Compare e descreva:

O que acontece quando um pacote se perde?
Como cada protocolo lida com múltiplos clientes?
Impacto da latência em cada implementação
Consumo de recursos (memória, CPU)
3. Threading no Contexto do Chat
Explique:

Por que threading é necessário?
Gerenciamento de threads (criação, término, limpeza)
Sincronização de threads (se necessário)
Modelo de gerenciado de fluxo de mensagens em caso de fila (organização)
Desafios comuns

 