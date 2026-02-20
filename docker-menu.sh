#!/bin/bash

echo "=== Sistema Cliente-Servidor TCP/UDP ==="
echo ""
echo "[1] Iniciar Servidor"
echo "[2] Ver Logs do Servidor"
echo "[3] Criar Cliente TCP"
echo "[4] Criar Cliente UDP"
echo "[5] Teste de Estresse TCP"
echo "[6] Teste de Estresse UDP"
echo "[7] Parar Servidor"
echo "[0] Sair"
echo ""
read -p "Opção: " opcao

case $opcao in
    1)
        echo "Iniciando servidor..."
        docker compose up -d servidor
        echo "✓ Servidor iniciado!"
        echo "Use opção [2] para ver os logs"
        ;;
    2)
        docker compose logs -f servidor
        ;;
    3)
        read -p "Nome do cliente TCP: " nome
        ./run-cliente-tcp.sh "$nome"
        ;;
    4)
        ./run-cliente-udp.sh
        ;;
    5)
        read -p "Clientes (padrão 5000): " clientes
        read -p "Mensagens (padrão 5): " mensagens
        clientes=${clientes:-5000}
        mensagens=${mensagens:-5}
        echo "Executando teste TCP..."
        docker compose --profile stress-test run --rm \
          -e TOTAL_CLIENTES=$clientes \
          -e MENSAGENS_POR_CLIENTE=$mensagens \
          teste-estresse-tcp
        ;;
    6)
        read -p "Clientes (padrão 500): " clientes
        read -p "Mensagens (padrão 100): " mensagens
        clientes=${clientes:-500}
        mensagens=${mensagens:-100}
        echo "Executando teste UDP..."
        docker compose --profile stress-test run --rm \
          -e TOTAL_CLIENTES=$clientes \
          -e MENSAGENS_POR_CLIENTE=$mensagens \
          teste-estresse-udp
        ;;
    7)
        docker compose down
        echo "✓ Servidor parado!"
        ;;
    0)
        exit 0
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac
