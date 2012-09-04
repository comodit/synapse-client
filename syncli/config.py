import sys
import ConfigParser

from os.path import expanduser, join, dirname, isfile, abspath


default_config = {
        "rabbitmq": {
            "endpoint": "localhost",
            "vhost": "/",
            "ssl_port": "5671",
            "port": "5672",
            "exchange": "amq.fanout",
            "consume_exchange": "",
            "queue": "",
            "username": "guest",
            "password": "guest",
            "use_ssl": False,
            "ssl_auth": False,
            "cacertfile": "",
            "certfile": "",
            "keyfile": ""
            },
        "logging": {
            "level": "DEBUG"
            }
        }


def get_config_path(filename):

    user_path = join(expanduser('~'), '.synapse-client', filename)
    etc_path = join("/etc/synapse", filename)
    curdir_path = abspath(join(dirname(__file__), '..', 'conf', filename))

    for loc in user_path, etc_path, curdir_path:
        if isfile(loc):
            return loc

# Here we update the default configuration with the settings in the
# config.
config = ConfigParser.SafeConfigParser()
try:
    config.read(get_config_path('synapse-client.conf'))
except ConfigParser.MissingSectionHeaderError, err:
    sys.exit(err)

for section in config.sections():
    if len(config.items(section)):
        default_config[section].update(dict(config.items(section)))


class AbstractConfig(object):
    """
    Abstract config class.
    This is the base class for all config classes.
    There is 1 config class per section in present in default_config.
    Contructor takes 1 argument which is the section name of the section.
    It creates dynamically the attributes, sets the default values
    and sets properties.
    """

    def __init__(self, section):
        for setting in default_config.get(section).iteritems():
            self._add_property(setting[0], setting[1])

    def _add_property(self, name, value):
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)

        setattr(self.__class__, name, property(fget, fset))
        setattr(self, '_' + name, value)

    def _set_property(self, name, value):
        setattr(self, '_' + name, value)

    def _get_property(self, name):
        return getattr(self, '_' + name)

    def __str__(self):
        nice_print = ['\n']
        for k, v in self.__dict__.iteritems():
            nice_print.append("%12s : %s" % (k.lstrip("_"), v))
        return "\n".join(nice_print)


class RabbitmqConfig(AbstractConfig):
    def __init__(self):
        super(RabbitmqConfig, self).__init__("rabbitmq")


class LoggingConfig(AbstractConfig):
    def __init__(self):
        super(LoggingConfig, self).__init__("logging")


class Config(object):
    """
    This class is a helper to access config options.
    Example:
    > config.rabbitmq.username
    to get rabbitmq username
    """

    def __init__(self):
        self.rabbitmq = RabbitmqConfig()
        self.logging = LoggingConfig()

config = Config()
