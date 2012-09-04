from syncli.api.transport import Amqp


class Client(object):

    def __init__(self, publish_queue, response_queue):
        self.publish_queue = publish_queue
        self.response_queue = response_queue

    def __enter__(self):
        self.connect()

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def connect(self):
        self.amqp = Amqp(self.publish_queue, self.response_queue)
        self.amqp.start()
        self.amqp.is_connected.wait()

    def send(self, msg):
        self.publish_queue.put(msg)

    def disconnect(self):
        self.amqp.is_connected.clear()
        self.publish_queue.put("stop")
        self.amqp.join()
