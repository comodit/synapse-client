Welcome to synapse-client hosts's documentation!
================================================

Synopsis
--------

`synapse-client hosts status` [--all] [--hostname] [--ip] [--mac_addresses] [--memtotal] [--platform] [--uptime]

Description
-----------

.. automodule:: syncli.cmd.hosts

Action
------

.. automethoddoc:: syncli.cmd.hosts.HostsCmd.status

Options
-------

--all
    Gets all options at once.

--hostname
    Retrieve the host's hostnames.

--ip
    Retrieve the hosts's ip addresses.

--mac_addresses
    Retrieves the host's mac addresses.

--memtotal
    Retrieves the hosts's total memory.

--platform
    Retrieves the hosts's linux platform.

--uptime
    Retrieves the host's uptime

Examples
--------

To get the status of current live machines:

.. code-block:: bash

    $ synapse-client hosts status --all

