Welcome to synapse-client packages's documentation!
===================================================

Synopsis
--------

`synapse-client packages install` <package>

`synapse-client packages remove` <package>

`synapse-client packages status` [<package>]

`synapse-client packages update` [<package>]

Description
-----------

.. automodule:: syncli.cmd.packages

`package` argument is the package name.

.. automethoddoc:: syncli.cmd.packages.PackagesCmd.install

.. automethoddoc:: syncli.cmd.packages.PackagesCmd.remove

.. automethoddoc:: syncli.cmd.packages.PackagesCmd.status

If no `package` is specified, retrieves all installed packages on the
remote systems.

.. automethoddoc:: syncli.cmd.packages.PackagesCmd.update

Examples
--------

Let's install htop on all alive machines:

.. code-block:: bash

    $ ./bin/synapse-client packages install htop

When can retrieve the status of the current installed package:

.. code-block:: bash

    $ ./bin/synapse-client packages status htop

To update everything on all alive machines:

.. code-block:: bash

    $ ./bin/synapse-client packages update

You can also specify a specific package to update:

.. code-block:: bash

    $ ./bin/synapse-client packages update htop

Finally, we remove the htop package.

.. code-block:: bash

    $ ./bin/synapse-client packages remove htop

