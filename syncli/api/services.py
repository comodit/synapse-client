from syncli.api.resources import Resources


class ServicesApi(Resources):

    _collection = "services"

    ######################
    ## Defining methods ##
    ######################

    def status(self, name):
        """Retrieves the status (running / enabled) of a service.

        @param name: The service name
        @type name: String
        """
        self.action = "read"
        self.name = name
        return self.request()

    def start(self, name, monitor=None):
        """Starts a service.

        @param name: The service name
        @type name: String

        @param monitor: Monitor this resource
        @type monitor: Boolean
        """
        self.action = "update"
        self.name = name
        self.monitor = monitor
        self.attributes["running"] = True
        return self.request()

    def restart(self, name):
        """Restarts a service.
        
        @param name: The service name
        @type name: String
        """
        self.action = "update"
        self.name = name
        self.attributes["restart"] = True
        return self.request()

    def reload(self, name):
        """Reloads a service.
        
        @param name: The service name
        @type name: String
        """
        self.action = "update"
        self.name = name
        self.attributes["reload"] = True
        return self.request()

    def stop(self, name, monitor=None):
        """Stops a service.
        
        @param name: The service name
        @type name: String

        @param monitor: Monitor this resource
        @type monitor: Boolean
        """
        self.action = "update"
        self.name = name
        self.monitor = monitor
        self.attributes["running"] = False
        return self.request()

    def enable(self, name, monitor=None):
        """Enables a service at boot.
        
        @param name: The service name
        @type name: String

        @param monitor: Monitor this resource
        @type monitor: Boolean
        """
        self.action = "update"
        self.name = name
        self.monitor = monitor
        self.attributes["enabled"] = True
        return self.request()

    def disable(self, name, monitor=None):
        """Disables a service at boot.
        
        @param name: The service name
        @type name: String

        @param monitor: Monitor this resource
        @type monitor: Boolean
        """
        self.action = "update"
        self.name = name
        self.monitor = monitor
        self.attributes["enabled"] = False
        return self.request()
