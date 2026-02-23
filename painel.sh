#!/bin/bash

# Limpa variáveis que causam erro de biblioteca no Ubuntu/Snap
unset LD_LIBRARY_PATH
unset PYTHONPATH

while true; do
    clear
    echo "======================"
    echo "  Painel de Controle"
    echo "======================"
    echo "|1| - Servidor Gateway"
    echo "|2| - Cliente TCP"
    echo "|3| - Cliente UDP"
    echo "|4| - Teste de Estresse TCP"
    echo "|5| - Teste de Estresse UDP"
    echo "|0| - Sair"
    echo "======================"
    read -p "Sua escolha: " escolha

    case $escolha in
        1)
            echo "Iniciando Servidor Gateway..."
            gnome-terminal -- bash -c "python3 servidor.py; exec bash"
            ;;
        2)
            read -p "Quantos clientes TCP? " qtd
            for ((i=1; i<=qtd; i++)); do
                gnome-terminal -- bash -c "python3 cliente_tcp.py; exec bash"
            done
            ;;
        3)
            read -p "Quantos clientes UDP? " qtd
            for ((i=1; i<=qtd; i++)); do
                gnome-terminal -- bash -c "python3 cliente_udp.py; exec bash"
            done
            ;;
        4)
            echo "Iniciando Teste de Estresse TCP..."
            gnome-terminal -- bash -c "python3 teste_estresse.py; exec bash"
            ;;
        5)
            echo "Iniciando Teste de Estresse UDP..."
            gnome-terminal -- bash -c "python3 teste_estresse_udp.py; exec bash"
            ;;
        0)
            echo "Saindo..."
            exit 0
            ;;
        *)
            echo "Escolha inválida! Pressione Enter para continuar."
            read
            ;;
    esac
done
