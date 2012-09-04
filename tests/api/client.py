import signal

from Queue import Queue

from syncli.api.client import Client

ayear = 365 * 24 * 60 * 60
STOPALRM = object()
PING_TIMEOUT = 3


class TestClient(object):

    def __init__(self, Api):
        signal.signal(signal.SIGALRM, self._alarm_handler)

        self.publish_queue = Queue()
        self.response_queue = Queue()
        self.disco_hosts = []

        self.client = Client(self.publish_queue, self.response_queue)
        self.api = Api(self.publish_queue, self.response_queue)

        self.client.connect()
        self.ping()

    def disconnect(self):
        self.client.disconnect()

    def send(self, msg):
        self.client.send(msg)

    def get_responses(self):
        """ Gets responses synchronously.
        """

        responses = []
        for i in range(len(self.disco_hosts)):
            resp = self.response_queue.get(True, ayear)
            if resp is STOPALRM:
                break

            responses.append(resp)

        return responses

    def ping(self):
        """ Sends a ping request the controller and sets the responses
        into self.disco_hosts.
        """

        # The future list of responses.
        responses = []

        # Discover available host through the API.
        req = self.api.ping()
        self.client.send(req)

        # Arm the... alarm :-)
        signal.alarm(PING_TIMEOUT)

        while True:
            # Listen for the responses
            resp = self.response_queue.get(True, ayear)
            if resp is STOPALRM:
                break

            responses.append(resp)

        # Store the list of discovered hosts.
        self.disco_hosts = responses

    def _alarm_handler(self, signum, frame):
        self.response_queue.put(STOPALRM)
