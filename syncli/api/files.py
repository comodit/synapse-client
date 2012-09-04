from syncli.api.resources import Resources


class FilesApi(Resources):
    _collection = "files"

    def infos(self, path, md5=False, content=False):
        """Retrieves the meta data of the file. Owner, group, mode,
        modification time.

        @param path: The file path
        @type path: String

        @param md5: Set this to True if the md5 hash must be retrieved.
        @type md5: bool

        @param content: Set this to True if the file content must be retrieved.
        @type content: bool
        """

        self.name = path
        self.action = "read"
        if md5:
            self.attributes["md5"] = True
        if content:
            self.attributes["get_content"] = True
        return self.request()

    def create(self, path, content=None, owner=None, group=None, mode=None,
               monitor=None):
        """Creates a file. Default mode is root:root 644.

        @param path: The file path
        @type path: str

        @param content: The content of the file. Default is empty.
        @type content: str

        @param owner: Sets the file owner
        @type owner: str

        @param group: Sets the file group
        @type group: str

        @param mode: Sets the file mode
        @type mode: str

        @param mode: Monitor this file
        @type mode: boolean
        """

        self.name = path
        self.action = 'create'
        self.monitor = monitor

        if content:
            self.attributes['content'] = content
        if owner:
            self.attributes['owner'] = owner
        if group:
            self.attributes['group'] = group
        if mode:
            self.attributes['mode'] = mode
        return self.request()

    def update_meta(self, path, owner=None,
                    group=None, mode=None, monitor=None):
        """Updates the meta data of a file.

        @param path: The file path
        @type path: str

        @param owner: Sets the file owner
        @type owner: str

        @param group: Sets the file group
        @type group: str

        @param mode: Sets the file mode
        @type mode: str

        @param mode: Monitor this file
        @type mode: boolean
        """

        self.name = path
        self.action = "update"
        self.monitor = monitor
        if owner:
            self.attributes["owner"] = owner
        if group:
            self.attributes["group"] = group
        if mode:
            self.attributes["mode"] = mode
        return self.request()

    def set_content(self, path, content, encoding=None, monitor=None):
        """Updates the content of a file with specified content. If the
        content is encoded, encoding parameter specifies the encoding type.

        @param path: The file path
        @type path: str

        @param content: The content
        @type content: str

        @param encoding: Encoding type of content. Default is none.
                         Available: base64
        @type encoding: str

        @param mode: Monitor this file
        @type mode: boolean
        """

        self.name = path
        self.monitor = monitor
        self.action = "update"
        self.attributes["content"] = content
        self.attributes["encoding"] = encoding
        return self.request()

    def set_content_from_url(self, path, url, encoding=None, monitor=None):
        """Same as L{set_content}, but content comes from a URL.

        @param path: The file path
        @type path: str

        @param url: The url from which content must be retrieved. The content is
        retrieved from the remote host, not from the client.
        @type url: str

        @param mode: Monitor this file
        @type mode: boolean
        """

        self.name = path
        self.action = "update"
        self.monitor = monitor
        self.attributes["content_by_url"] = url
        self.attributes["encoding"] = encoding
        return self.request()

    def delete(self, path, monitor=None):
        """Deletes a file.

        @param path: The file path
        @type path: str

        @param mode: Monitor this file
        @type mode: boolean
        """

        self.name = path
        self.action = "delete"
        self.monitor = monitor
        return self.request()
