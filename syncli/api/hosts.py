from syncli.api.resources import Resources


class HostsApi(Resources):
    """
    This is the hosts controller. It's basically used to retrieve informations
    about hosts connected to the broker.
    """

    _collection = "hosts"
    _attrs = ("ip",
              "hostname",
              "mac_addresses",
              "uptime",
              "memtotal",
              "platform")

    def infos(self, attrs=list()):
        """ Retrieves information about a host.

        @param attrs: A list of host's attributes must be retrieved.
        See L{_attrs} for available attributes.
        @type attrs: list or tuple
        """

        self.action = 'read'
        self.attributes = [attr for attr in attrs if attr in self._attrs]
        return self.request()
