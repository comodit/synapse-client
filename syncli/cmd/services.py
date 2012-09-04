""" Manipulate the service resource
"""

from syncli.exceptions import ControllerException
from syncli.router import register
from syncli.cmd.generic import GenericCmd
from syncli.api.services import ServicesApi


@register(ServicesApi)
class ServicesCmd(GenericCmd):

    attributes = (("status", []),
                  ("start", []),
                  ("restart", []),
                  ("reload", []),
                  ("stop", []),
                  ("enable", []),
                  ("disable", []),)

    def status(self, argv):
        """ Gets the service status (enable/disabled).
        """

        options, name = self._get_options(argv, "status")

        self.do_action('status', name)

    def start(self, argv):
        """ Starts the service.
        """

        options, name = self._get_options(argv, "start")
        if not name:
            raise ControllerException("Please specify the service name.")

        mon = self.get_mon_value(options)
        self.do_action('start', name, monitor=mon)

    def restart(self, argv):
        """ Restarts the service.
        """

        options, name = self._get_options(argv, "restart")
        if not name:
            raise ControllerException("Please specify the service name.")

        mon = self.get_mon_value(options)
        self.do_action('restart', name, monitor=mon)

    def reload(self, argv):
        """ Reloads the service.
        """

        options, name = self._get_options(argv, "reload")
        if not name:
            raise ControllerException("Please specify the service name.")

        mon = self.get_mon_value(options)
        self.do_action('reload', name, monitor=mon)

    def stop(self, argv):
        """ Stops the service.
        """

        options, name = self._get_options(argv, "stop")
        if not name:
            raise ControllerException("Please specify the service name.")

        mon = self.get_mon_value(options)
        self.do_action('stop', name, monitor=mon)

    def enable(self, argv):
        """ Enables the service at boot.
        """

        options, name = self._get_options(argv, "enable")
        if not name:
            raise ControllerException("Please specify the service name.")

        mon = self.get_mon_value(options)
        self.do_action('enable', name, monitor=mon)

    def disable(self, argv):
        """ Disables the service at boot.
        """

        options, name = self._get_options(argv, "disable")
        if not name:
            raise ControllerException("Please specify the service name.")

        mon = self.get_mon_value(options)
        self.do_action('disable', name, monitor=mon)
