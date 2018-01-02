#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socketserver
import json
import redis

redisclients = {}


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        # cur_thread = threading.current_thread()

        try:
            jdata = json.loads(data)
            host = str(jdata[0]['host'])
            port = int(jdata[0]['port'])
            command = str(jdata[0]['command'])
            print('host: %s, port: %d, command: %s' % (host, port, command))
            print('start connect redis')
            node = host + ':' + str(port)
            reply = None
            if node in redisclients:
                print("redis connection %s have created" % node)
                r = redisclients[node]
                reply = r.execute_command(command)
            else:
                print("create a new redis connection %s" % node)
                r = redis.StrictRedis(host=host, port=port)
                reply = r.execute_command(command)
                redisclients[node] = r

            self.request.sendall(reply)
        except Exception as e:
            print('connect node %s error %s', node)
            errmessage = ('Read json data error: %s' % str(e))
            response = bytes(errmessage, encoding='utf-8')
            # delete bad redis connection
            if node in redisclients:
                print('remove node %s from redisclients' % node)
                del redisclients[node]
            self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 8808

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.serve_forever()
