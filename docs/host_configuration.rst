Advanced host configuration
===========================

Host side configuration
-----------------------

It is possible to tweak the host configuration by putting a `.airsd.cfg` file at the
root of the storage host. This file must follow the "INI" format:

.. code-block:: ini

    [DEFAULT]
    option1=value1
    option2=value2

Possible options are:

* `compression`: The compression to use when sending an archive with the `--archive`
  argument of the `airfs put` command. Can be `gz` (Gzip), `bz2` (Bzip2) or `xz` (LZMA).
  Default to `gz`.
* `files_directory`: Path to directory where are stored the files on the host.
  This path is relative to the storage host root. Default to `files`
* `max_expiry`: Maximum expiration value allowed. This value follow the same format
  as the `--expiry` argument of the `airfs put` command. Default to `0` (No limit).
* `random_prefix`: Enable the random prefix between the `files_directory` and the file
  name. This allow to avoid collision of files with an identical name by providing an
  unique path for all files. Default to True.

Client side configuration
-------------------------

Since airfs is a client only solution, all values of the storage host configuration file
can also be defined client side using the `airfs configure` command.

It is possible to configure multiple host at the same time by specifying the host while
setting an option:

.. code-block:: bash

    airsd configure --host https://my_storage.com OPTION VALUE

The airfs client always uses storage host configuration file values over any client
configuration.

Recommended permissions
-----------------------

The following permissions are recommended.

Senders
~~~~~~~~
Read and write access is required to the directory where shared files are stored
(`files`, or the value defined with the `files_directory` option)

If the sender needs to use the `airsd delete`, the deletion access is also required.
Note that there is no mechanism to prevent the deletion of a file by another user.

If the storage host configuration file is used (`.airsd.cfg`), read-only access is
required.

Recipients
~~~~~~~~~~

Recipient does not require any access to the storage host.

Files lifecycle and expiration
------------------------------

Storage generally does not provide a feature to automatically delete a single file after
some expiration.

Some storage provides lifecycles feature that can be applied to some prefixes or
directories. This allow to automatically delete files on specified rules. It is possible
to use this with airsd to ensure expired files are deleted after a delay. This delay
must be set to a value that is a comfortable maximum to use with airsd.

It is possible to set the airsd `max_expiry` configuration value to this delay to inform
the airsd client that it must raise an error if an user tries to use a longer expiration
value.

airsd also provide the `airsd delete` command to manually delete a file.
