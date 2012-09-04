""" Manipulate the file resource on remote systems.
"""

import tempfile
import base64
import os
import sys

from syncli.util import editor, fmt
from syncli.cmd.generic import GenericCmd
from syncli.exceptions import ControllerException
from syncli.router import register
from syncli.api.files import FilesApi


@register(FilesApi)
class Files(GenericCmd):
    """ This is the files resource.
    """

    attributes = (("status", [{"name": "get_content",
                               "option_action": "store_true",
                               "help": "Retrieves the content of the file."},
                              {"name": "save",
                               "option_action": "store",
                               "help": "Saves the file on the disk with " \
                                   "temporary name in /tmp folder."},
                              {"name": "md5",
                               "help": "Retrieves the MD5 sum of the file",
                               "option_action": "store_true"}]),
                  ("create", [{"name": "owner",
                               "help": "Sets the file owner",
                               "option_action": "store"},
                              {"name": "group",
                               "help": "Sets the file group",
                               "option_action": "store"},
                              {"name": "mode",
                               "help": "Sets the file mode",
                               "option_action": "store"},
                              {"name": "content",
                               "help": "Sets the content of the file",
                               "option_action": "store"}]),
                  ("edit", [{"name": "force",
                             "option_action": "store_true",
                             "help": "If md5 hashes of files content " \
                                 "differ, it will force the update"}]),
                  ("update_meta", [{"name": "owner",
                                    "help": "Updates the file owner",
                                    "option_action": "store"},
                                    {"name": "group",
                                    "help": "Updates the file group",
                                    "option_action": "store"},
                                   {"name": "mode",
                                    "help": "Updates the file mode",
                                    "option_action": "store"}]),
                  ("set_content", [{"name": "from_url",
                                    "help": "Set the content from http",
                                    "option_action": "store"},
                                   {"name": "from_file",
                                    "help": "Set the content from a file " \
                                        "on disk",
                                    "option_action": "store"},
                                   {"name": "from_string",
                                    "help": "Set the content from the " \
                                        "command line",
                                    "option_action": "store"}]),
                  ("delete", []))

    def status(self, argv):
        """ Retrieves the meta data of a file.
        """

        options, path = self._get_options(argv, 'status')

        if not path:
            raise ControllerException("Please specify the file name.")

        kwargs = {'content': options.get('get_content'),
                  'md5': options.get('md5')}

        get_content = options.get('get_content')
        md5 = options.get('md5')

        if options.get('save'):
            get_content = True

        # Build the request
        request = self.api.infos(path, content=get_content, md5=md5)

        # When the "save" option is provided, get the responses synchronously,
        # as we don't have to print the results.
        if options.get('save'):
            with self.client:
                self.ping()
                self.client.send(request)
                self._save_files(self.get_responses(), options['save'])
        else:
            self.do_action('infos', path, **kwargs)

    def _save_files(self, responses, path):
        for resp in responses:
            if not resp.get('error'):
                filename = os.path.basename(resp['status']['name'])
                folder = os.path.join(os.path.abspath(path), resp['uuid'])
                try:
                    os.makedirs(folder, 0755)
                except OSError:
                    pass
                filepath = os.path.join(folder, filename)
                try:
                    with open(filepath, 'w') as fd:
                        fd.write(resp['status']['content'])
                except IOError as err:
                    raise ControllerException(err)

                print "File content saved to %s" % filepath
            else:
                fmt.pprint(resp)

    def create(self, argv):
        """ Creates a file on remote hosts.
        """

        options, path = self._get_options(argv, 'create')
        if not path:
            raise ControllerException("Please specify the file name.")

        attributes = self._get_attrs('create', options)
        mon = self.get_mon_value(options)
        self.do_action('create', path, monitor=mon, **attributes)

    def edit(self, argv):
        """ Edits a file "remotely". It's opened in $EDITOR.
        """

        options, path = self._get_options(argv, 'edit')
        if not path:
            raise ControllerException("Please specify the file name.")

        responses = []
        nb_hosts = 0
        request = self.api.infos(path, md5=True, content=True)

        with self.client:
            self.ping()

            nb_hosts = len(self.disco_hosts)
            if nb_hosts:
                self.client.send(request)
                responses = self.get_responses()
            else:
                return

        mon = self.get_mon_value(options)

        if len(responses):
            # Gets the first md5.
            md5 = responses[0].get('status').get('md5')

            can_edit = True
            for resp in responses:
                if resp.get('status').get('md5') != md5:
                    print "\nSorry, you can't update because files differ " \
                        "on hosts."
                    print "You could use the --force, Luke, to bypass this " \
                        "limitation."
                    can_edit = False

            if options.get('force') or can_edit:
                resp = responses[0].get('status')
                if not resp.get('error'):
                    path = resp.get('name', path)
                    starting_text = resp.get('content', ' ')
                    try:
                        content = editor.edit_text(starting_text) or ' '
                        self.client.connect()
                        request = self.api.set_content(path, content,
                                                       monitor=mon)
                        self.client.send(request)
                        self.get_responses()
                        self.client.disconnect()
                    except editor.NotModifiedException:
                        print "File not modified."

    def update_meta(self, argv):
        """ Updates the meta-data (owner, group, mode) of a file.
        """
        options, path = self._get_options(argv, 'update_meta')
        if not path:
            raise ControllerException("Please specify the file name.")

        if not options:
            self.print_options('update_meta')
            raise ControllerException("Please specify an option !")

        attributes = self._get_attrs('update_meta', options)

        mon = self.get_mon_value(options)
        self.do_action('update_meta', path, monitor=mon, **attributes)

    def set_content(self, argv):
        """Sets the content of a file."""

        options, path = self._get_options(argv, 'set_content')

        if not path:
            raise ControllerException("Please specify the file name.")

        from_file = options.get('from_file')
        from_url = options.get('from_url')
        from_string = options.get('from_string')
        mon = self.get_mon_value(options)
        content = None

        if from_file:
            content = self._get_content_from_file(from_file)
            self.do_action('set_content', path, content)

        elif from_url:
            self.do_action('set_content_from_url', path, from_url)

        elif from_string:
            content = base64.b64encode(from_string)
            self.do_action('set_content', path, content, encoding='base64')

        else:
            print "No content specified"

    def _get_content_from_file(self, filename):
        content = None
        try:
            fd = open(filename, 'rb')
            content = fd.read()
            #content = base64.b64encode(content)
        except IOError, err:
            print "Error while opening", filename
            print "[%s]" % err
            sys.exit(1)
        except TypeError:
            pass

        return content

    def delete(self, argv):
        """Deletes a file."""

        options, path = self._get_options(argv, 'delete')
        mon = self.get_mon_value(options)

        if not path:
            raise ControllerException("Please specify the file name.")

        self.do_action('delete', path, monitor=mon)

    def _print(self, resp, get_content=False):

        # Avoid to pprint the content attribute.
        fmt.pprint(resp, ignore_attrs=['content'])

        if get_content:
            print('--')
            print resp.get('status').get('content')
            sys.stdout.write('--\n')
