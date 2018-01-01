#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import json


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, encoding='utf-8'))
        response = str(sock.recv(1024), encoding='utf-8')
        print("Received: {}".format(response))


if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 8808
    node1 = [{"host": "127.0.0.1", "port": 2000, "command": "ping"}]
    node2 = [{"host": "127.0.0.1", "port": 2001, "command": "ping"}]
    node3 = [{"host": "127.0.0.1", "port": 2002, "command": "ping"}]

    client(ip, port, json.dumps(node1))
    client(ip, port, json.dumps(node2))
    client(ip, port, json.dumps(node3))

    node2 = [{"host": "127.0.0.1", "port": 2001, "command": "info"}]
    client(ip, port, json.dumps(node2))