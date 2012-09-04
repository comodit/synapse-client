Welcome to synapse-client services's documentation!
===================================================

Synopsis
--------

`synapse-client services status` <service>

`synapse-client services start` <service>

`synapse-client services restart` <service>

`synapse-client services reload` <service>

`synapse-client services stop` <service>

`synapse-client services enable` <service>

`synapse-client services disable` <service>


Description
-----------

.. automodule:: syncli.cmd.services

`service` argument is the service name.

Actions
-------

.. automethoddoc:: syncli.cmd.services.ServicesCmd.status

.. automethoddoc:: syncli.cmd.services.ServicesCmd.start

.. automethoddoc:: syncli.cmd.services.ServicesCmd.restart

.. automethoddoc:: syncli.cmd.services.ServicesCmd.reload

.. automethoddoc:: syncli.cmd.services.ServicesCmd.stop

.. automethoddoc:: syncli.cmd.services.ServicesCmd.enable

.. automethoddoc:: syncli.cmd.services.ServicesCmd.disable

Examples
--------

Suppose you would like to start the `rsyslog` service:

.. code-block:: bash

    $ ./bin/synapse-client services status rsyslog

Then, you would like to start the service:

.. code-block:: bash

    $ ./bin/synapse-client services start rsyslog

Finally, you would like to have the service started on boot:

.. code-block:: bash

    $ ./bin/synapse-client services enable rsyslog

