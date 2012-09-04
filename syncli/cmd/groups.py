""" Manipulate the group resource.
"""

from syncli.exceptions import ControllerException
from syncli.cmd.generic import GenericCmd
from syncli.api.groups import GroupsApi
from syncli.router import register


@register(GroupsApi)
class GroupsCmd(GenericCmd):

    attributes = (('status', []),
                  ('create', []),
                  ('update', [{'name': 'new_name',
                               'help': 'The new name of the group.'}]),
                  ('remove', []))

    def status(self, argv):
        """ Retrieves the group informations.
        """

        options, name = self._get_options(argv, 'status')

        self.do_action('infos', name)

    def create(self, argv):
        """ Creates a group.
        """

        options, name = self._get_options(argv, 'create')
        if not name:
            raise ControllerException("Please specify the group name")

        self.do_action('create', name)

    def update(self, argv):
        """ Updates a group.
        """

        options, name = self._get_options(argv, 'update')
        if not name:
            raise ControllerException("Please specify the group name")

        _new_name = options.get('new_name')

        self.do_action('update', name, _new_name)

    def remove(self, argv):
        """ Removes a group.
        """

        options, name = self._get_options(argv, 'remove')
        if not name:
            raise ControllerException("Please specify the group name")

        self.do_action('remove', name)
