from syncli.api.resources import Resources


class CommandsApi(Resources):
    _collection = 'executables'
    _attributes = ('command',)

    def execute(self, command):
        """ Executes a command remotely.
        """

        self.action = 'update'
        self.name = command
        return self.request()
