# Python TCP Client A
import socket

host = '127.0.0.1'
port = 8808
BUFFER_SIZE = 2000
MESSAGE = input("tcpClientA: Enter message/ Enter exit:")

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))

while MESSAGE != 'exit':

    tcpClientA.send(bytes(MESSAGE, encoding='utf-8'))
    data = tcpClientA.recv(BUFFER_SIZE)
    print("Received: {}".format(data))
    MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:")

tcpClientA.close()