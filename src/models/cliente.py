from socket import socket
from typing import Any, Tuple


class Cliente:
    def __init__(self, id_usuario, socket: socket, endereco: Tuple[Any, ...]):
        self.id_usuario = id_usuario
        self.username = ""
        self.socket = socket
        self.endereco = endereco
