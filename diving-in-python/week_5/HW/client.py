import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, ip, port, timeout=None):
        self._ip = ip
        self._port = int(port)
        self._timeout = int(timeout)

        try:
            self._sock = socket.create_connection((self._ip, self._port), self._timeout)
        except socket.error as ex:
            raise ClientError("Error with creating connection", ex)

    def __del__(self):
        try:
            self._sock.close()
        except socket.error as ex:
            raise ClientError("Error with closing", ex)

    def get(self, metric):
        try:
            self._sock.sendall(f'get {metric}\n'.encode('utf-8'))
            recv = str(self._sock.recv(1024).decode('utf-8'))
        except socket.error as ex:
            raise ClientError("Error with get", ex)

        if 'ok\n' != recv[0:3]:
            raise ClientError

        data = dict()
        lines = recv.split('\n')

        for line in lines[1:-2]:
            try:
                metric, value, timestamp = line.split()
                if metric not in data:
                    data[metric] = []
                data[metric].append((int(timestamp), float(value)))
                data[metric].sort(key=lambda tup: tup[0])
            except Exception as ex:
                raise ClientError(ex, "Error with get")

        return data

    def put(self, metric, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        try:
            self._sock.sendall(f"put {metric} {value} {timestamp}\n".encode('utf-8'))
            if 'ok\n' not in self._sock.recv(1024).decode('utf-8'):
                raise ClientError
        except socket.error as ex:
            raise ClientError("Error with put", ex)
