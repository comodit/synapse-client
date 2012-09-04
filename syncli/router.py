import os
import sys
import imp
import pkgutil

from syncli import cmd
from syncli import options
from syncli.exceptions import ControllerException
from syncli.options import parser
from syncli.logger import logger


@logger
class Router(object):

    resource = None

    def dispatch(self, argv):

        if '--version' in argv:
            print options.get_version()
            return

        # Handle resource completion
        if '--completion' in argv:
            self.resource_completion(argv)

        # Avoid to complete options when no [resource action] are
        # specified.
        if '--completion-option' in argv and len(argv) <= 3:
            return

        # If there's no arguments or the --help argument without
        # anything else, print the doc and exit.
        if len(argv) == 0 or argv[0] == '--help':
            self.print_resources()
            sys.stdout.write('\n')
            parser.parse_args()
            return

        # Load the resource module specified in the cmdline.
        self._load_resource(argv[0])

        if self.resource:
            # Pass the remaining cmdline arguments.
            self.resource.run(argv[1:])
        else:
            raise ControllerException("Resource '%s' is not loaded" % argv[0])

    def resource_completion(self, argv):
        if len(argv) <= 2:
            ret_list = []

            for loader, modname, ispkg in pkgutil.iter_modules(cmd.__path__):
                if not ispkg and modname != 'generic':
                    ret_list.append(modname)
                    if modname in argv:
                        return None

            # Print the resource list and exit.
            print ' '.join(ret_list)
            sys.exit(0)

    def print_resources(self):
        print "Available resources:"
        for loader, modname, ispkg in pkgutil.iter_modules(cmd.__path__):
            if not ispkg and modname != 'generic':
                print "  " + modname

    def _load_resource(self, resource_name):
        """
        """

        # Gets the path of the resources package.
        dirname = os.path.dirname(cmd.__file__)

        try:
            # Finds the module of the current resource in dirname.
            fp, pathname, desc = imp.find_module(resource_name, [dirname])

            # Loads the found module.
            imp.load_module(resource_name, fp, pathname, desc)
        except ImportError as e:
            self.print_resources()
            self.logger.error(e)
            sys.exit(1)


router = Router()


def register(res_api_cls=None):
    def f(res_cli_cls):
        res_cli = res_cli_cls()

        if res_api_cls:
            res_api = res_api_cls(res_cli.publish_queue,
                                  res_cli.response_queue)
            setattr(res_cli, 'api', res_api)

        Router.resource = res_cli
        return res_cli_cls
    return f
