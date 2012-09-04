import logging
import logging.config

from syncli.config import get_config_path
from syncli import options
from syncli.router import router
from syncli.exceptions import ControllerException, ArgumentException


def run(argv):
    # Configures the logger
    logging.config.fileConfig(get_config_path('synapse-client-logger.conf'))
    logging.getLogger('syncli').setLevel(logging.DEBUG)

    options.init()

    try:
        router.dispatch(argv)
        exit(0)
    except ControllerException as e:
        print e
    except ArgumentException as e:
        print e.msg

    # TODO: Print the traceback on debug.
