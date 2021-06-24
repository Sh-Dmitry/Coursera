import asyncio

STORAGE = dict()


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()




class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def process_data(self, command):

        if command.strip('\n').strip() == '':
            return 'error\nwrong command\n\n'

        elements = command.split()

        if elements[0] == 'get':
            if len(elements) == 2:
                return self._get(elements[1])
            return 'error\nwrong command\n\n'
        elif elements[0] == 'put':
            if len(elements) == 4:
                return self._put(elements[1], elements[2], elements[3])
            return 'error\nwrong command\n\n'
        else:
            return 'error\nwrong command\n\n'

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def _get(self, key):

        send_metrics = 'ok\n'
        if key == '*':
            for key, item_list in STORAGE.items():
                item_list.sort()
                for item_tuple in item_list:
                    try:
                        send_metrics += f'{key} {item_tuple[1]} {item_tuple[0]}\n'
                    except IndexError:
                        return 'Index error'
            return send_metrics + '\n'

        metrics_list = STORAGE.get(key, None)

        if metrics_list is None:
            return 'ok\n\n'

        try:
            metrics_list.sort()
            for metric in metrics_list:
                send_metrics += f'{key} {metric[1]} {metric[0]}\n'
            return send_metrics + '\n'
        except IndexError:
            return 'Index error'

    def _put(self, key, value, timestamp):
        if key == '*':
            return 'error\nkey cannot contain *\n\n'

        try:
            value, timestamp = float(value), int(timestamp)
        except ValueError:
            return 'error\nwrong command\n\n'

        old_metrics_list = STORAGE.get(key, [])
        for i, metric in enumerate(old_metrics_list):
            if metric[0] == timestamp:
                old_metrics_list.remove((timestamp, metric[1]))
                old_metrics_list.insert(i, (timestamp, value))
                return 'ok\n\n'

        old_metrics_list.append((timestamp, value))
        STORAGE.update({key: old_metrics_list})

        return 'ok\n\n'



