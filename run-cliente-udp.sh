#!/bin/bash

echo "Iniciando cliente UDP"

docker run -it --rm \
  --network desafio-sistema-servidor-tcp-udp_rede-comunicacao \
  -e ALVO_IP=servidor \
  -e ALVO_PORTA=5555 \
  desafio-sistema-servidor-tcp-udp-servidor \
  python cliente_udp.py
