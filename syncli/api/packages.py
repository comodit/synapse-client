from syncli.api.resources import Resources


class PackagesApi(Resources):
    _collection = "packages"

    def status(self, name=None):
        """Retrieves if the package is installed or not intalled on remote
        hosts. If name is not specified, a list of installed packages is
        retrieved (can be resource consuming).

        @param name: The name of the package
        @type name: String
        """

        self.action = "read"
        self.name = name
        return self.request()

    def install(self, name, monitor=None):
        """Installs a package.

        @param name: The name of the package
        @type name: String

        @param monitor: Monitor this resource
        @type monitor: Boolean
        """

        self.action = "create"
        self.name = name
        self.monitor = monitor
        return self.request()

    def update(self, name=None, monitor=None):
        """Updates a package. Updates the system if name is not provided.

        @param name: The name of the package
        @type name: String

        @param monitor: Monitor this resource
        @type monitor: Boolean
        """

        self.action = "update"
        self.name = name
        self.monitor = monitor
        return self.request()

    def remove(self, name, monitor=None):
        """Removes a package.

        @param name: The name of the package
        @type name: String

        @param monitor: Monitor this resource
        @type monitor: Boolean
        """

        self.action = "delete"
        self.name = name
        self.monitor = monitor
        return self.request()
