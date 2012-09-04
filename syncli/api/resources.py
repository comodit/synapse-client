import uuid

from syncli.logger import logger
from syncli.exceptions import ArgumentException
from syncli.api.filters import filters


def required(*required_attrs):
    def wrap(f):
        def wrapped_f(*args):
            for required in required_attrs:
                if required not in args[2]:
                    raise ArgumentException("Please specify the argument: %s" \
                                                % required)
            return f(*args)
        return wrapped_f
    return wrap


@logger
class Resources(object):
    def __init__(self, publish_queue, response_queue):
        self.publish_queue = publish_queue
        self.response_queue = response_queue
        self.attributes = {}
        self.name = ''
        self.action = 'read'
        self.monitor = None

    def ping(self):
        self.action = 'ping'
        return self.request()

    def reset(self):
        self.attributes = {}

    def handle_response(self, response):
        raise Exception("Not implemented yet !")

    def request(self):
        corr_id = str(uuid.uuid4())

        attrs = self.attributes
        request = {
            'action': self.action,
            'collection': self._collection,
            'id': self.name,
            'correlation_id': corr_id,
            'attributes': attrs
        }

        if self.monitor is not None:
            request['monitor'] = self.monitor

        # Inject the filters into the request
        request['filters'] = filters

        self.reset()
        return request
