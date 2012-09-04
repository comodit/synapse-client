from syncli.util.bcolors import UnixColor


def pprint(resp, ignore_attrs=[]):
    """ Displays a pretty print of the reponses.
    ignore_attrs contains a list of ignore attributes (this attributes
    will not be printed).
    """

    if isinstance(resp, dict):
        status = resp.get('status', {})
        pprint_uuid(resp['uuid'])
        pprint_attrs(status, ignore_attrs)
        pprint_error(resp.get('error'))
    else:
        print resp


def colorize(color, msg):
    """ Surrounds the msg with the unix color.
    """

    return color + msg + UnixColor.ENDC


def pprint_uuid(uuid):
    """ Displays a pretty print of the UUID of the machine.
    """

    # Configures the colorize.
    color = UnixColor.BOLD + UnixColor.OKGREEN

    # Displays the message and reset colorize settings.
    print colorize(color, '[' + uuid + ']')


def pprint_attrs(status, ignore_attrs=[]):
    """ Displays a pretty print of all status attributes.
    """

    # Configures the color.
    color = UnixColor.BOLD

    if isinstance(status, dict):
        # Gets the all the status keys.
        keys = status.keys()

        # Computes the number of spaces to align correctly the
        # output.
        spaces = 1
        if keys:
            spaces = len(max(keys, key=len)) + 1

        for attr in keys:
            if attr not in ignore_attrs:
                # Formats the message with correct number of spaces.
                attr_formatted = '{0:{1}}'.format(attr, spaces)
                print colorize(color, attr_formatted) + '%s' % status[attr]

        print ''
    elif isinstance(status, list):
        for elem in status:
            pprint_attrs(elem)
    else:
        print colorize(color, "Status") + ' %s' % status


def pprint_error(error):
    """ Prints the error if there's an error.
    """

    if error:
        print colorize(UnixColor.BOLD, "Error") + ' %s' % error


def pprint_col(items):
    """
    """

    # Gets the list of names from items
    names = [item[0] for item in items]

    if names:
        # Computes the number of spaces.
        spaces = len(max(names, key=len)) + 2

    for name, desc in items:
        print '  {0:{1}}{2}'.format(name, spaces, desc)
