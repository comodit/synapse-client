from syncli.api.resources import Resources


class PluginsController(Resources):

    _collection = "plugins"

    def infos(self, name=None):
        self.action = "read"
        if name:
            self.name = name
        return self.request()
