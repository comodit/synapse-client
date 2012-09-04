Welcome to synapse-client hosts's documentation!
================================================

Synopsis
--------

`synapse-client files create` <path> [--content <content>] [--group <group>] [--mode <mode>] [--owner <owner>]

`synapse-client files edit` <path> [--force]

`synapse-client files delete` <path>

`synapse-client files set_content` <path> [(--from_url | --from_file | --from_string) <source>]

`synapse-client files status` <path> [--get_content] [--save] [--md5]

`synapse-client files update_meta` <path> [--owner] [--group] [--mode]


Description
-----------

.. automodule:: syncli.cmd.files

<path> is the fullpath of the file.

Actions
-------

.. automethoddoc:: syncli.cmd.files.Files.create

.. automethoddoc:: syncli.cmd.files.Files.edit

If the specified `path` file is not the same (computed with md5sum) on
all remote systems, the edition cannot be done except if the --force
argument is present. In this case, the file will be edited with the
content of the first file response received.

.. automethoddoc:: syncli.cmd.files.Files.delete

.. automethoddoc:: syncli.cmd.files.Files.set_content

.. automethoddoc:: syncli.cmd.files.Files.status

.. automethoddoc:: syncli.cmd.files.Files.update_meta

Options
-------

--content
    Specify the content of the file.

--force
    If md5 hashes of files content differ, it will force the update.

--from_file
    Set the content of the file from a fullpath on the local system. (`source`)

--from_string
    Set the content of the file from a string. (`source`)

--from_url
    Set the content of the file from a http url (`source`)

--get_content
    Get the content of the file.

--group
    The group.

--md5
    Retrieves the MD5 digest of the file.

--mode
    The file permission.

--owner
    The owner user.

--save
    Saves the file on the disk with temporary name in /tmp folder (on Unix).

Examples
--------

Create a `/tmp/foo` file with root:root owner/group and 755 permission. The
content is set to "Hello world" during the creation.

.. code-block:: bash

    $ synapse-client files create /tmp/foo --owner root --group root --mode 755
    -- content "Hello world"

Then, the status returns the attributes of the file:

.. code-block:: bash

    $ synapse-client files status /tmp/foo

To retrieve the content of the file, specify the --get_content option.

.. code-block:: bash

    $ synapse-client files status /tmp/foo --get_content

Then, you can modify the file content with the `set_content` action.


.. code-block:: bash

    $ synapse-client files set_content /tmp/foo --set_content --from_string
    "Hello everybody"

You can edit the content with your favorite editor ($EDITOR).

.. code-block:: bash

    $ synapse-client edit /tmp/foo

Then, you can change the metadata of the file.

.. code-block:: bash

    $ synapse-client update_meta --owner chuck --group norris

Finally, you can delete the file.

.. code-block:: bash

    $ synapse-client delete /tmp/foo
