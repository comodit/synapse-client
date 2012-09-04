Welcome to synapse-client commands's documentation!
===================================================

Synopsis
--------

`synapse-client commands execute` <cmd>

Description
-----------

.. automodule:: syncli.cmd.commands

`cmd` argument is the raw command.

Action
------

.. automethoddoc:: syncli.cmd.commands.CommandsCmd.execute

Example
-------

.. code-block:: bash

    $ synapse-client commands execute "ls -l ~/"
