""" Manipulate the host resource.
"""

from syncli.cmd.generic import GenericCmd
from syncli.router import register
from syncli.api.hosts import HostsApi


@register(HostsApi)
class HostsCmd(GenericCmd):

    attributes = (('status', [{'name': 'ip',
                               'help': "Retrieves the host's ip addresses",
                               'option_action': 'store_true'},
                              {'name': 'hostname',
                               'help': "Retrieves the host's hostnames",
                               'option_action': 'store_true'},
                              {'name': 'mac_addresses',
                               'help': "Retrieves the host's mac addresses",
                               'option_action': 'store_true'},
                              {'name': 'memtotal',
                               'help': "Retrieves the host's total memory",
                               'option_action': 'store_true'},
                              {'name': 'platform',
                               'help': "Retrieves the host's linux platform",
                               'option_action': 'store_true'},
                              {'name': 'uptime',
                               'help': "Retrieves the host's uptime",
                               'option_action': 'store_true'},
                              {'name': 'all',
                               'option_action': 'store_true',
                               'help': "Gets all options at once"}]),)

    def status(self, argv):
        """ Gets the status of reacheable hosts.
        """

        options, name = self._get_options(argv, 'status')

        opts = []
        if not options.get('all'):
            opts = [k for k, v in options.iteritems()]
        else:
            opts = [opts['name'] for opts in self.attributes[0][1]]

        self.do_action('infos', opts)
