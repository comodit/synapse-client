""" Manipulate raw command on remote systems.
"""

from syncli.cmd.generic import GenericCmd
from syncli.exceptions import ControllerException
from syncli.router import register
from syncli.api.commands import CommandsApi


@register(CommandsApi)
class CommandsCmd(GenericCmd):

    attributes = (('execute', []),)

    def execute(self, argv):
        """ Executes a raw command on the remote system.
        """

        options, command = self._get_options(argv, 'execute')
        if not command:
            raise ControllerException("Please specify a command")

        self.do_action('execute', command)
