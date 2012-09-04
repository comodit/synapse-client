import sys
import logging
import signal
import optparse

from Queue import Queue

from syncli.api.client import Client
from syncli.util import fmt
from syncli.options import parser
from syncli.exceptions import ControllerException
from syncli.logger import logger


ayear = 365 * 24 * 60 * 60
STOPALRM = object()
STOP = object()
PING_TIMEOUT = 1


@logger
class GenericCmd(object):

    # TODO: Useful ?
    attributes = []

    def __init__(self):
        """
        """

        signal.signal(signal.SIGINT, self._sigint_handler)
        signal.signal(signal.SIGALRM, self._alarm_handler)

        self.options = None

        self._actions = {}
        self.register_actions()

        self.publish_queue = Queue()
        self.response_queue = Queue()
        self.wait_queue = Queue()
        self.client = Client(self.publish_queue, self.response_queue)
        self.disco_hosts = []

    def wait(self):
        """Use this method to wait after using the client.connect() method
        """
        self.wait_queue.get(True, ayear)

    def get_mon_value(self, options):
        _mon = None
        if options.get("monitor"):
            _mon = True
        if options.get("unmonitor"):
            _mon = False
        return _mon

    def run(self, argv):
        """
        """

        self.action_completion(argv)

        if len(argv) == 0:
            print "Please specify an action.\n"
            self._print_actions()
        elif argv[0] == '--help':
            self._print_actions()
        else:
            action = argv[0]
            if action in self._actions:
                remaining_args = argv[1:]

                # Call the resource method associated to this action.
                self._actions[action](remaining_args)
            else:
                raise ControllerException("%s is not a valid action." % action)

    def action_completion(self, argv):
        if len(argv) <= 2 and '--completion' in argv:
            res = []
            for key in self._actions:
                res.append(key)
                if key in argv:
                    return

            print ' '.join(res)
            sys.exit(0)

    def option_completion(self, argv, action):
        if '--completion-option' in argv:
            opts_list = self._get_options_list(action)
            if len(opts_list):
                # Don't display already given arguments.
                print ' '.join(list(set(opts_list) - set(argv)))

            # Completion done. Bye !
            sys.exit(0)

        # Exit on completion mode. We don't want synapse-client to
        # execute anything on this mode.
        if '--completion' in argv:
            sys.exit(0)

    def _get_attrs(self, action, options):
        ret = {}

        opts = self._get_method_attrs(action)
        for opt in opts:
            opt_name = opt['name']

            if options.get(opt_name):
                ret[opt_name] = options.get(opt_name)

        return ret

    def _get_options_list(self, action):
        opts = self._get_method_attrs(action)
        return ['--%s' % opt['name'] for opt in opts]

    def do_action(self, method, *args, **kwargs):
        # Build the request according to the method and args.
        request = getattr(self.api, method)(*args, **kwargs)

        # Connect the client.
        with self.client:
            # Send the ping.
            self.ping()

            # Send the request if there's at least 1 host.
            if len(self.disco_hosts):
                # Send the request.
                self.client.send(request)

                # Print the response asynchronously.
                self.print_responses()

    def register_actions(self):
        """ Maps action name with action method. The names must
        match.
        """

        for action, options in self.attributes:
            self._actions[action] = getattr(self, action)

    def _print_actions(self):
        print "Available actions:"

        to_print = []
        for key in self._actions:
            raw_desc = self._actions[key].__doc__ or ''
            desc = ' '.join(raw_desc.split())

            to_print.append((key, desc))

        fmt.pprint_col(to_print)

    def _get_options(self, argv, action_name):
        """
        """

        # Get option completion.
        self.option_completion(argv, action_name)

        # Remove the auto-generated help option.
        parser.remove_option('--help')

        # Add custom help options.
        parser.add_option('--help',
                          dest='help',
                          action='store_true',
                          default=None)

        attributes = self._get_method_attrs(action_name)

        if attributes:
            for option in attributes:
                parser.add_option('--%s' % option.get('name'),
                        dest=option.get('name'),
                        action=option.get('option_action', 'store'),
                        default=option.get('default', None),
                        help=optparse.SUPPRESS_HELP)
        else:
            attributes = []

        # Here we go, parse the arg !
        try:
            self.options, args = parser.parse_args(argv)
        except UnboundLocalError:
            raise ControllerException("Please specify an argument")


        # Sets the logger level according to the -v options.
        level = logging.DEBUG if self.options.debug else logging.INFO
        syncli_logger = logging.getLogger('syncli')
        syncli_logger.setLevel(level)

        if level == 'INFO':
            for handler in syncli_logger.handlers:
                formatter = logging.Formatter('%(message)s')
                handler.setFormatter(formatter)

        # 1) Transforms OptParse options to dict.
        # 2) Remove the entry if the value is None.
        self.options = dict((k, v) for k, v in vars(self.options).iteritems() \
                                if v is not None)

        # Display the help for this action ?
        if self.options.get('help'):
            self.print_options(action_name)

            # TODO: Raise an exception ? Are you sure ?
            raise ControllerException()

        return self.options, args[0] if len(args) else None

    def _get_method_attrs(self, method_name):
        for item in self.attributes:
            if method_name in item:
                return item[1]
        return []

    def print_options(self, method_name):
        self.options = self._get_method_attrs(method_name)
        if len(self.options):
            print "Available options:"

            to_print = []
            for opt in self.options:
                to_print.append(('--%s' % opt.get('name'),
                                 opt.get('help', 'No help provided.')))

            fmt.pprint_col(to_print)
        else:
            print "No option available, sorry !"

    def print_responses(self):
        """ Gets responses and displays them asynchronously.
        """

        try:
            for i in range(len(self.disco_hosts)):
                resp = self.response_queue.get(True, ayear)
                if resp in (STOP, STOPALRM):
                    break

                fmt.pprint(resp)
        finally:
            # At the end, dont't forget to reset the number of
            # discovered host.
            self.disco_hosts = []

    def get_responses(self):
        """ Gets responses synchronously.
        """

        responses = []
        try:
            for i in range(len(self.disco_hosts)):
                resp = self.response_queue.get(True, ayear)
                if resp in (STOP, STOPALRM):
                    break

                responses.append(resp)
        finally:
            # At the end, dont't forget to reset the number of
            # discovered host.
            self.disco_hosts = []
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
            if resp is STOP:
                return []
            elif resp is STOPALRM:
                break

            responses.append(resp)

        # Store the list of discovered hosts.
        self.disco_hosts = responses

        num_hosts = len(responses)
        host_plural = 'hosts' if num_hosts > 1 else 'host'
        self.logger.info("Discovered %s %s..." % (num_hosts, host_plural))

    def _alarm_handler(self, signum, frame):
        self.response_queue.put(STOPALRM)

    def _sigint_handler(self, signum, frame):
        mess = "Killed x__x"
        print '\b\b%s%s' % (mess, '\b' * len(mess))
        self.wait_queue.put(True)
        self.publish_queue.put("stop")
        self.response_queue.put(STOP)
        self.client.disconnect()
