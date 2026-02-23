#!/bin/bash

if [ -z "$1" ]; then
    read -p "Nome do cliente: " NOME
else
    NOME=$1
fi

echo "Iniciando cliente TCP: $NOME"

docker run -it --rm \
  --network desafio-sistema-servidor-tcp-udp_rede-comunicacao \
  -e ALVO_IP=servidor \
  -e ALVO_PORTA=5555 \
  desafio-sistema-servidor-tcp-udp-servidor \
  bash -c "echo '$NOME' | python cliente_tcp.py; exec bash"
