import optparse

from optparse import OptionGroup

from syncli.config import config
from syncli.api.filters import filters


class MyOptionParser(optparse.OptionParser):
    def error(self, msg):
        pass

usage = "usage: %prog resource action id [options]"

parser = MyOptionParser(usage=usage)


def get_version():
    syncli_version = "Undefined"
    try:
        import syncli.version as version_mod
        if version_mod.VERSION:
            syncli_version = version_mod.VERSION
    except (ImportError, AttributeError):
        pass
    return syncli_version

def _multi_filters_callback(option, opt, value, parser):
    for fil in value.split(','):
        args = {opt.split('_')[1]: value.split(',')}
        filters.update(**args)


def setup_filters_options():
    filters_group = OptionGroup(parser, "Filters")

    filters_group.add_option("--filter_uuids",
                             dest="uuids",
                             type="string",
                             action="callback",
                             default=None,
                             callback=_multi_filters_callback,
                             help="Filters these comma separated uuids")

    filters_group.add_option("--filter_hostnames",
                             type="string",
                             dest="hostnames",
                             action="callback",
                             callback=_multi_filters_callback,
                             default=None,
                             help="Filters these comma separated hostnames")

    filters_group.add_option("--filter_macaddresses",
                             type="string",
                             dest="macaddresses",
                             default=None,
                             action="callback",
                             callback=_multi_filters_callback,
                             help="Filter these comma separated mac_addresses")

    filters_group.add_option("--filter_ipaddresses",
                             type="string",
                             dest="ips",
                             default=None,
                             action="callback",
                             callback=_multi_filters_callback,
                             help="Filter these comma separated ip_addresses")

    parser.add_option_group(filters_group)


def setup_debug_options():
    debug_group = OptionGroup(parser, "Debug options")

    debug_group.add_option("-v",
                           dest="debug",
                           help="display debug information",
                           action="store_true",
                           default=False)

    parser.add_option_group(debug_group)


def amqp_options_callback(option, opt, value, parser):
    setattr(config.rabbitmq, option.dest, value)


def setup_collections_options():
    collections_group = OptionGroup(parser, "Global collections options")

    collections_group.add_option("--monitor",
                                 dest="monitor",
                                 action="store_true",
                                 help="Monitor resource")

    collections_group.add_option("--unmonitor",
                                 dest="unmonitor",
                                 action="store_true",
                                 help="Unmonitor resource")

    parser.add_option_group(collections_group)


def setup_amqp_options():
    amqp_group = OptionGroup(parser, "Amqp options")

    amqp_group.add_option("--vhost",
                          dest="vhost",
                          type="string",
                          action="callback",
                          callback=amqp_options_callback,
                          default=config.rabbitmq.vhost,
                          help="Rabbitmq vhost")

    amqp_group.add_option("--target",
                          dest="queue",
                          type="string",
                          action="callback",
                          callback=amqp_options_callback,
                          default=config.rabbitmq.queue,
                          help="Direct Message a host")

    amqp_group.add_option("--exchange",
                          dest="exchange",
                          type="string",
                          action="callback",
                          callback=amqp_options_callback,
                          default=config.rabbitmq.exchange,
                          help="Exchange in which the message will be "
                          "published")

    amqp_group.add_option("--broker",
                          dest="endpoint",
                          type="string",
                          action="callback",
                          callback=amqp_options_callback,
                          default=config.rabbitmq.endpoint,
                          help="Endpoint for the API. Default to localhost")

    amqp_group.add_option("--user",
                          dest="username",
                          type="string",
                          action="callback",
                          callback=amqp_options_callback,
                          default=config.rabbitmq.username,
                          help="Username on rabbitmq server. Default: guest")

    amqp_group.add_option("--pass",
                          dest="password",
                          type="string",
                          action="callback",
                          callback=amqp_options_callback,
                          default=config.rabbitmq.password,
                          help="Password on rabbitmq server. Default: guest")

    parser.add_option_group(amqp_group)


def setup_completions_options():
    comp_group = OptionGroup(parser, 'Completion options')

    comp_group.add_option('--completion',
                          dest='completion',
                          action='store_true',
                          help=optparse.SUPPRESS_HELP)

    parser.add_option_group(comp_group)


def init():
    setup_filters_options()
    setup_debug_options()
    setup_amqp_options()
    setup_collections_options()
    setup_completions_options()
