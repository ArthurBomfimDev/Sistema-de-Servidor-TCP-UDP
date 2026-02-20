#!/bin/bash

echo "Iniciando cliente UDP"

docker run -it --rm \
  --network desafio-sistema-servidor-tcp-udp_rede-comunicacao \
  -e HOST=servidor \
  -e PORT=5555 \
  desafio-sistema-servidor-tcp-udp-servidor \
  python cliente_udp.py
