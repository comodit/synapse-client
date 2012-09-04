""" Manipulate the user resource.
"""

from syncli.exceptions import ControllerException
from syncli.cmd.generic import GenericCmd
from syncli.router import register
from syncli.api.users import UsersApi


@register(UsersApi)
class UsersCmd(GenericCmd):

    attributes = (("status", []),
                  ("create", [{"name": "password",
                               "option_action": "store"},
                              {"name": "login_group",
                               "option_action": "store"},
                              {"name": "groups",
                               "option_action": "store"}]),
                  ("update", [{"name": "password",
                               "option_action": "store"},
                              {"name": "login_group",
                               "option_action": "store"},
                              {"name": "add_to_groups",
                               "option_action": "store"},
                              {"name": "remove_from_groups",
                               "option_action": "store"},
                              {"name": "set_groups",
                               "option_action": "store"}]),
                  ("remove", []))

    def status(self, argv):
        """ Retrieves a user's informations.
        """

        options, name = self._get_options(argv, "status")

        if not name:
            raise ControllerException("Please specify the user name.")

        self.do_action('infos', name)

    def create(self, argv):
        """ Creates a user.
        """

        options, name = self._get_options(argv, "create")

        if not name:
            raise ControllerException("Please specify the user name.")

        if not options:
            self.print_options("create")
            raise ControllerException("Please specify options.")

        _password = options.get("password")
        _login_group = options.get("login_group")
        _groups = options.get("groups")
        mon = self.get_mon_value(options)
        self.do_action('create', name, _password,
                       _login_group, _groups, monitor=mon)

    def update(self, argv):
        """ Updates a user.
        """

        options, name = self._get_options(argv, "update")

        if not name:
            raise ControllerException("Please specify the user name.")

        if not options:
            self.print_options(self.attributes)
            raise ControllerException("Please specify options.")

        _password = options.get("password")
        _login_group = options.get("login_group")
        _add_to_groups = options.get("add_to_groups")
        _remove_from_groups = options.get("remove_from_groups")
        _set_groups = options.get("set_groups")

        mon = self.get_mon_value(options)
        self.do_action('update', name, _password, _login_group,
                       _add_to_groups, _remove_from_groups, _set_groups, mon)

    def remove(self, argv):
        """ Removes a user.
        """

        options, name = self._get_options(argv, "remove")

        if not name:
            raise ControllerException("Please specify the user name.")

        mon = self.get_mon_value(options)
        self.do_action('remove', name, mon)
