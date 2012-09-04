Welcome to synapse-client services's documentation!
===================================================

Synopsis
--------

`synapse-client services status` <service>

`synapse-client services update` <service> [(--disable | --enable | --reload | --restart | --start | --stop)]



Description
-----------

.. automodule:: syncli.cmd.services

`service` argument is the service name.

Actions
-------

.. automethoddoc:: syncli.cmd.services.ServicesCmd.status

.. automethoddoc:: syncli.cmd.services.ServicesCmd.update

Examples
--------

Suppose you would like to start the `rsyslog` service:

.. code-block:: bash

    $ ./bin/synapse-client services status rsyslog

Then, you would like to start the service:

.. code-block:: bash

    $ ./bin/synapse-client services update rsyslog --start

Finally, you would like to have the service started on boot:

.. code-block:: bash

    $ ./bin/synapse-client services update rsyslog --enable


