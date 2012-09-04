Welcome to synapse-client group's documentation!
================================================

Synopsis
--------

`synapse-client create` <group>

`synapse-client update` <group> --newname <name>

`synapse-client status` [<group>]

`synapse-client remove` <group>


Description
-----------

.. automodule:: syncli.cmd.groups

`group` argument is the group name.

Actions
-------

.. automethoddoc:: syncli.cmd.groups.GroupsCmd.create

.. automethoddoc:: syncli.cmd.groups.GroupsCmd.status

If the `group` is not specified, lists all groups on remote systems.

.. automethoddoc:: syncli.cmd.groups.GroupsCmd.update

`name` argument is the new name to assign the `group` name.

.. automethoddoc:: syncli.cmd.groups.GroupsCmd.remove

Examples
--------

Let's create a group named `foo`.


.. code-block:: bash

    $ synapse-client groups create foo

To retrieve the metadata of the created group:

.. code-block:: bash

    $ synapse-client groups status foo

Then, let's rename the `foo` group to the `foo2` group.

.. code-block:: bash

    $ synapse-client groups update foo --new_name foo2

Finally, remove the `foo2` group.

.. code-block:: bash

    $ synapse-client groups remove foo2
