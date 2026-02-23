#!/bin/bash

while true; do
    clear
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
            ;;
        2)
            env -u LD_LIBRARY_PATH gnome-terminal -- bash -c "docker compose logs -f servidor; exec bash"
            echo "✓ Logs abertos em novo terminal"
            ;;
        3)
            read -p "Digite quantos clientes TCP deseja iniciar: " quantidade
            for ((i=1; i<=quantidade; i++)); do
                env -u LD_LIBRARY_PATH gnome-terminal -- bash -c "docker compose run --rm cliente-tcp; exec bash"
            done
            echo "✓ $quantidade cliente(s) TCP foram iniciados em novo terminal"
            ;;
        4)
            read -p "Digite quantos clientes UDP deseja iniciar: " quantidade
            for ((i=1; i<=quantidade; i++)); do
                env -u LD_LIBRARY_PATH gnome-terminal -- bash -c "docker compose run --rm cliente-udp; exec bash"
            done
            echo "✓ $quantidade cliente(s) UDP foram iniciados em novo terminal"
            ;;
        5)
            env -u LD_LIBRARY_PATH gnome-terminal -- bash -c "docker compose run --rm teste-estresse-tcp"
            echo "✓ Teste TCP iniciado em novo terminal"
            ;;
        6)
            env -u LD_LIBRARY_PATH gnome-terminal -- bash -c "docker compose run --rm teste-estresse-udp"
            echo "✓ Teste UDP iniciado em novo terminal"
            ;;
        7)
            echo "Parando servidor e limpando a rede..."
            docker compose down --remove-orphans
            echo "✓ Servidor parado!"
            ;;
        0)
            echo "Saindo do painel..."
            exit 0
            ;;
        *)
            echo "Opção inválida!"
            ;;
    esac
done