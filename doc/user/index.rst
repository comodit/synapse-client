Welcome to synapse-client users's documentation!
================================================

Synopsis
--------

`synapse-client users create` <user> [--groups <groups] [--login_group <login_group>] [--password <passwd>]

`synapse-client users remove` <user>

`synapse-client users status` <user>

`synapse-client users update` <user> [--add_to_groups <groups>] [--set_groups <groups>] [--remove_from_groups <groups>] [--login_group <login_group>] [--password <passwd>]

Description
-----------

.. automodule:: syncli.cmd.users

`user` argument is the username.

Actions
-------

.. automethoddoc:: syncli.cmd.users.UsersCmd.create

.. automethoddoc:: syncli.cmd.users.UsersCmd.remove

.. automethoddoc:: syncli.cmd.users.UsersCmd.status

.. automethoddoc:: syncli.cmd.users.UsersCmd.update

Options
-------

--add_to_groups
    Add the user to this list of groups. `groups` argument is a list
    of comma separated group name.

--groups
    The user groups. `groups` argument is a list of comma separated
    group name.

--login_group
    The user login group.

--password
    The user password.

--set_groups
    Sets the user to this list of groups. `groups` argument is a list
    of comma separated group name.

--remove_from_groups
    Remove the user from this list of groups. `groups` argument is a
    list of comma separated group name.

Examples
--------

Let's create a user named `foo`.


.. code-block:: bash

    $ synapse-client users create foo

To retrieve the metadata of the created user:

.. code-block:: bash

    $ synapse-client users status foo

Then, let's change the `foo` password to 'secret'.

.. code-block:: bash

    $ synapse-client users update foo --password secret

You can also add a group to the user.

.. code-block:: bash

    $ synapse-client users update foo --add_to_groups group1,group2

Finally, remove the `foo` user.

.. code-block:: bash

    $ synapse-client users remove foo
