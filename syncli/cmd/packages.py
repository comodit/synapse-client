""" Manipulate the package resource.
"""

from syncli.cmd.generic import GenericCmd
from syncli.router import register
from syncli.api.packages import PackagesApi


@register(PackagesApi)
class PackagesCmd(GenericCmd):

    attributes = (("status", []),
                  ("install", []),
                  ("update", []),
                  ("remove", []))

    def status(self, argv):
        """ Retrieves the installed status of a package.
        """

        options, name = self._get_options(argv, 'status')
        self.do_action('status', name)

    def install(self, argv):
        """ Installs a package.
        """

        options, name = self._get_options(argv, "install")

        mon = self.get_mon_value(options)
        self.do_action('install', name, mon)

    def update(self, argv):
        """ Updates a package.
        """

        options, name = self._get_options(argv, "update")

        mon = self.get_mon_value(options)
        self.do_action('update', name, mon)

    def remove(self, argv):
        """ Removes a package.
        """

        options, name = self._get_options(argv, "remove")

        mon = self.get_mon_value(options)
        self.do_action('remove', name, mon)
