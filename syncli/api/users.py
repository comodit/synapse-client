from syncli.api.resources import Resources


class UsersApi(Resources):

    _collection = "users"

    def infos(self, name):
        """Retrieves informations about a user.
        gid, uid, name, dir, shell, gecos, groups

        @param name: The user name
        @type name: str
        """

        self.action = "read"
        self.name = name
        return self.request()

    def create(self, name, password=None,
               login_group=None, groups=None, monitor=None):
        """Creates user on the system.

        @param name: The username
        @type name: str

        @param password: The user password
        @type password: str

        @param login_group: The user's initial login group
        @type login_group: str

        @param groups: A list of supplementary groups which the user is also a member of
        @type groups: list

        @param monitor: Monitor this resource
        @type login_group: boolean
        """
        self.action = "create"
        self.name = name
        self.monitor = monitor
        if password:
            self.attributes["password"] = password
        if login_group:
            self.attributes["login_group"] = login_group
        if groups:
            self.attributes["groups"] = ','.join(groups)
        return self.request()

    def update(self, name,
               password=None,
               login_group=None,
               add_to_groups=None,
               remove_from_groups=None,
               set_groups=None,
               monitor=None):
        """Updates a user on the system.

        @param name: The username
        @type name: str

        @param password: The user password
        @type password: str

        @param add_to_groups: Add these groups to existing user's groups
        @type add_to_groups: list

        @param remove_from_groups: Remove users from these groups
        @type remove_from_groups: list

        @param set_groups: Set these groups to the user. Resets groups the
        user is already in.
        @type set_groups: list

        @param monitor: Monitor this resource
        @type login_group: boolean
        """

        self.action = "update"
        self.name = name
        self.monitor = monitor

        if password:
            self.attributes["password"] = password
        if login_group:
            self.attributes["login_group"] = login_group
        elif add_to_groups:
            self.attributes["add_to_groups"] = add_to_groups
        elif remove_from_groups:
            self.attributes["remove_from_groups"] = remove_from_groups
        elif set_groups:
            self.attributes["set_groups"] = set_groups

        return self.request()

    def remove(self, name, monitor=None):
        """ Removes a user from the system.

        @param name: The user's name
        @type name: str

        @param monitor: Monitor this resource
        @type login_group: boolean
        """

        self.action = "delete"
        self.monitor = monitor
        self.name = name
        return self.request()
