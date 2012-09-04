import threading
import pika
import time
import json
import sys

from pprint import pformat
from Queue import Empty
from ssl import CERT_REQUIRED

from pika import PlainCredentials
from pika import SelectConnection
from pika.adapters.select_connection import SelectPoller

from syncli.config import config
from syncli.logger import logger


class ExternalCredentials(PlainCredentials):
    """ The PlainCredential class is extended to work with external rabbitmq
    auth mechanism. Here, the rabbitmq-auth-mechanism-ssl plugin than can be
    found here http://www.rabbitmq.com/plugins.html#rabbitmq_auth_mechanism_ssl

    Rabbitmq's configuration must be adapted as follow :
    [
    {rabbit, [
     {auth_mechanisms, ['EXTERNAL']},
     {ssl_listeners, [5671]},
     {ssl_options, [{cacertfile,"/etc/rabbitmq/testca/cacert.pem"},
                    {certfile,"/etc/rabbitmq/server/cert.pem"},
                    {keyfile,"/etc/rabbitmq/server/key.pem"},
                    {verify,verify_peer},
                    {fail_if_no_peer_cert,true}]}
    ]}
    ].
    """
    TYPE = 'EXTERNAL'

    def __init__(self):
        self.erase_on_connect = False

    def response_for(self, start):
        if ExternalCredentials.TYPE not in start.mechanisms.split():
            return None, None
        return ExternalCredentials.TYPE, ""

    def erase_credentials(self):
        pass

# As mentioned in pika's PlainCredentials class, we need to append the new
# authentication mechanism to VALID_TYPES
pika.credentials.VALID_TYPES.append(ExternalCredentials)


class AmqpException(Exception):
    pass


@logger
class Amqp(threading.Thread):
    def __init__(self, publish_queue, response_queue):
        threading.Thread.__init__(self)

        try:
            self.port = int(config.rabbitmq.port)
            self.ssl_port = int(config.rabbitmq.ssl_port)
        except ValueError, err:
            sys.exit(err)

        self.endpoint = config.rabbitmq.endpoint
        self.vhost = config.rabbitmq.vhost
        self.exchange = config.rabbitmq.exchange
        self.queue = config.rabbitmq.queue
        self.username = config.rabbitmq.username
        self.password = config.rabbitmq.password
        self.use_ssl = config.rabbitmq.use_ssl
        self.ssl_auth = config.rabbitmq.ssl_auth
        self.cacertfile = config.rabbitmq.cacertfile
        self.certfile = config.rabbitmq.certfile
        self.keyfile = config.rabbitmq.keyfile
        self.consume_exchange = config.rabbitmq.consume_exchange

        self.response_queue = response_queue
        self.publish_queue = publish_queue

        self.connection = None
        self.channel = None

        self.is_connected = threading.Event()
        self.manual_close = False

        self.corr_id = None
        self.response = None
        self.reply_queue = None

    def run(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        ssl_options = None
        port = self.port

        if self.use_ssl:
            port = self.ssl_port

        if self.use_ssl and self.ssl_auth:
            ssl_options = {
                    "ca_certs": self.cacertfile,
                    "certfile": self.certfile,
                    "keyfile": self.keyfile,
                    "cert_reqs": CERT_REQUIRED
                    }
            credentials = ExternalCredentials()

        try:
            parameters = pika.ConnectionParameters(host=self.endpoint,
                                                   port=port,
                                                   virtual_host=self.vhost,
                                                   credentials=credentials,
                                                   ssl=self.use_ssl,
                                                   ssl_options=ssl_options)
        except TypeError:
            parameters = pika.ConnectionParameters(host=self.endpoint,
                                                   port=port,
                                                   virtual_host=self.vhost,
                                                   credentials=credentials)

        self.logger.debug("Connecting to %s@%s:%s on vhost %s" % (
                self.username, self.endpoint, port, self.vhost))

        try:
            SelectPoller.TIMEOUT = .1
            connection = SelectConnection(parameters)
            connection.add_on_close_callback(self._on_closed())
            connection.callbacks.add(0, '_on_connection_open',
                                     self._on_connected(), one_shot=True)
            self.connection = connection
            connection.ioloop.start()

        except IOError, err:
            if not self.manual_close:
                self.logger.error("Connection error: {0}".format(err))

        except pika.exceptions.LoginError, err:
            self.logger.error("Login Error: %s" % err)
        except KeyError, err:
            pass
        except AmqpException as err:
            self.logger.error("Amqp exception: %s" % err)
        except Exception, err:
            self.logger.error("Unknown exception: %s" % err)
        finally:
            # Release the event lock and close the connection
            self.is_connected.set()
            self.close()

    def _on_closed(self):
        def on_closed(connection):
            connection.ioloop.stop()
            self.is_connected.clear()
        return on_closed

    def close(self):
        self.is_connected.clear()
        connection = self.connection
        try:
            if connection and connection.is_open:
                connection.close()
                # It raises weird exceptions while closing the connection
                # when the following is uncommented. Examples from pika github
                # recommand it though.
                connection.ioloop.start()
        except IOError, err:
            self.logger.error("IOError in thread %s: %s" % \
                                  (self.getName(), err))
        except KeyError:
            pass

    def log_callback(self, frame):
        reply_code = str(frame.method.reply_code)
        reply_text = frame.method.reply_text
        msg = "[%s] %s" % (reply_code, reply_text)
        self.logger.debug("Frame: %s " % frame)

        raise AmqpException(msg)

    def _on_connected(self):
        def on_connected(connection):
            self.logger.debug("Connected to RabbitMQ on %s" % self.endpoint)
            connection.channel(self._on_channel_open())
            self.connection = connection
        return on_connected

    def _on_channel_open(self):
        def on_channel_open(channel):
            self.channel = channel
            self.connection.callbacks.add(channel.channel_number,
                    pika.spec.Channel.Close, self.log_callback)

            # Declare anonymous queue in which messages will be received.
            # We don't need this queue to last after all responses are received
            # hence the following settings.
            self.channel.queue_declare(queue='',
                                       durable=False,
                                       exclusive=False,
                                       auto_delete=True,
                                       callback=self._on_queue_declare())
        return on_channel_open

    def _on_queue_declare(self):
        def on_queue_declare(frame):
            self.reply_queue = frame.method.queue
            if self.consume_exchange:
                self.logger.debug("Binding to exchange %s" %
                                  self.consume_exchange)
                self.channel.queue_bind(queue=self.reply_queue,
                                        exchange=self.consume_exchange,
                                        routing_key=self.reply_queue,
                                        callback=self._on_queue_bound())
            else:
                self.logger.debug("Consuming on %s" % self.reply_queue)
                self.is_connected.set()
                self.channel.basic_consume(self._handle_delivery(),
                                           queue=self.reply_queue)
                self.connection.add_timeout(.1, lambda: self._publisher())

        return on_queue_declare

    def _on_queue_bound(self):
        def on_queue_bound(frame):
            self.logger.debug("Consuming on %s" % self.reply_queue)
            self.is_connected.set()
            self.channel.basic_consume(self._handle_delivery(),
                                       queue=self.reply_queue)
            self.connection.add_timeout(.1, lambda: self._publisher())
        return on_queue_bound

    def _handle_publish(self, message):
        exchange = message.get('exchange', self.exchange)
        corr_id = message.get('correlation_id')
        message.update(dict(timestamp=time.strftime('%d/%m/%y %H:%M:%S',
                                                    time.localtime())))
        for item in ['reply_to', 'correlation_id']:
            try:
                del message[item]
            except (KeyError, AttributeError):
                pass
        user_id = self.username or None
        headers = {'reply_exchange': self.consume_exchange}
        props = pika.BasicProperties(correlation_id=corr_id,
                                     user_id=user_id,
                                     reply_to=self.reply_queue,
                                     headers=headers)

        if not self.queue:
            self.logger.debug('Publishing into exchange [%s] with routing '
                              'key [%s] and corr_id [%s]:\n%s' %
                              (exchange,
                               self.queue,
                               corr_id, pformat(message)))
        else:
            self.logger.debug('Publishing directly into queue '
                              '[%s] with corr_id [%s]:\n%s' %
                              (self.queue,
                               corr_id, pformat(message)))

        params = {
            'properties': props,
            'body': json.dumps(message),
            'exchange': exchange,
            'routing_key': self.queue,
        }

        self.channel.basic_publish(**params)

    def _publisher(self):
        try:
            message = self.publish_queue.get(False)
            if message == "stop":
                self.close()
                return
            self._handle_publish(message)
        except Empty:
            pass
        finally:
            self.connection.add_timeout(1, lambda: self._publisher())

    def _handle_delivery(self):
        def handle_delivery(channel, method_frame, header_frame, body):
            # First thing, send the ack
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            response = json.loads(body)
            response.update({'correlation_id': header_frame.correlation_id})
            self.response_queue.put(response)
        return handle_delivery
