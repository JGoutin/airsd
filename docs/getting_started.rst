Getting Started
===============

Installation
------------

Supported Python versions: >= 3.6

Installation is performed using PIP:

.. code-block:: bash

    pip install airsd

All mandatory dependencies are automatically installed.

To use some storage, it is required to also install airfs with the required extra
dependencies.

Example of installing airsd and airfs with all dependencies:

.. code-block:: bash

    pip install airsd airfs[all]

Usage
-----

Airsd allow a sender user to share a file to a recipient user by storing it on the
sender's own storage over the cloud.

Airsd can be used as a command line utility and a Python API.

The following section shows the most common uses of the command line utility.
It is possible to get more information on the utility with the `airsd --help` command,
or `airsd SUBCOMMAND --help` for more information on a sub command (For instance
`airsd put --help` for more information on the `put` sub-command).

The Python API use is identical, refer to the API documentation for more information.

.. note::
  A storage host needs to be configured prior to use it with airsd.

  Some storage may require credentials to be used. See the selected storage
  `airfs documentation <https://airfs.readthedocs.io>`_ for more information.


Share files
~~~~~~~~~~~

The put command allows to copy a file to the storage host and return the shareable URL
that can be sent to the recipient:

.. code-block:: bash

    airsd put path/to/my_file --host https://my_storage.com/
    > https://my_storage.com/files/123456/my_file#token=123456

On the first call, the `--host` argument is required to specify the host to use. Then
airsd will use the last value used as default and the command can be simplified:

.. code-block:: bash

    airsd put path/to/my_file

To configure a fixed default host value:

.. code-block:: bash

    airsd configure default_host https://my_storage.com

To send a file archived:

.. code-block:: bash

    airsd put path/to/my_file --archive
    > https://my_storage.com/files/123456/my_file.tar.gz#token=123456

To send multiple files or directory in a single command (all files will be stored in a
single archive in this case):

.. code-block:: bash

    airsd put path/to/my_file path/to/my_file2 path/to/my_directory
    > https://my_storage.com/files/123456/archive.tar.gz#token=123456

To set an expiration time to the shareable link. After this delay, the recipient will
not be able to download the file. (By default airsd set this expiration to 1 day, a
reasonable and secure delay):

.. code-block:: bash

    # Expire after 120 seconds
    airsd put path/to/my_file --expire 120s

    # Expire after 10 minutes
    airsd put path/to/my_file --expire 10m

    # Expire after 6 hours
    airsd put path/to/my_file --expire 6h

    # Expire after 30 days
    airsd put path/to/my_file --expire 30d


Airsd also allow to share a file from another airfs supported storage:

.. code-block:: bash

    airsd put https://my_storage.com/my_file

.. warning::
    `--archive` and multiple sources in a single command are currently not supported
    with non local files.

Get shared files
~~~~~~~~~~~~~~~~

Shareable link can be used with any web browser or commands like `curl` or `wget`, thus
airsd provides a `get` function for convenience.

To download the file in the current directory:

.. code-block:: bash

    airsd get https://my_storage.com/files/123456/my_file#token=123456

To download the file to a specific location:

.. code-block:: bash

    airsd get https://my_storage.com/files/123456/my_file#token=123456 --output path/to/my_file

To download and extract an archived file:

.. code-block:: bash

    airsd get https://my_storage.com/files/123456/my_file.tar.gz#token=123456 --extract


Delete shared files
~~~~~~~~~~~~~~~~~~~

The sender can delete a shared file using the following command:

.. code-block:: bash

    airsd delete https://my_storage.com/files/123456/my_file#token=123456

Storage host configuration
--------------------------

The airsd storage host does not require a specific configuration to work. Just ensure
the storage host, bucket/container must exist before airsd use and senders have the
proper read and write access to it.

Once ready, the absolute path or URL of the storage must be provided to senders
and used with the `--host` argument of the `airfs put` command.

The host root can be a subdirectory inside the storage.

See `airfs documentation <https://airfs.readthedocs.io>`_ for more information on
storage.
