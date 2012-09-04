from syncli.api.resources import Resources


class GroupsApi(Resources):

    _collection = "groups"

    def infos(self, name):
        """Retrieves informations about a group.

        @param name: The group name
        @type name: str
        """

        self.action = "read"
        self.name = name
        return self.request()

    def create(self, name, monitor=None):
        """Creates user on the system.

        @param name: The group name
        @type name: str

        """
        self.action = "create"
        self.name = name
        return self.request()

    def update(self, name, new_name):
        """Updates a user on the system.

        @param name: The group name
        @type name: str

        @param new_name: The new group name
        @type password: str
        """

        self.action = "update"
        self.name = name

        if new_name:
            self.attributes["new_name"] = new_name

        return self.request()

    def remove(self, name):
        """ Removes a group from the system.

        @param name: The groups's name
        @type name: str
        """

        self.action = "delete"
        self.name = name
        return self.request()

