airsd: Simple file sharing in the cloud
=======================================

Airsd (Air send) is a simple file sharing utility.

It allows sharing files using your own cloud storage as the only backend. No web server
or extra services are required, this also mean no maintenance and minimal costs.

Airsd uses shareable URL features of cloud storage to give access to the privately
stored file to the recipient.

It also provides the following features:

* Easy to use command line interface.
* Send files from local storage or any `Airfs <https://github.com/JGoutin/airfs>`_
  supported storage.
* Send files and directories as archives.
* URL link expiration delay.
* Python API to use it from your own code.

Supported storage hosts
------------------------

A cloud storage is required to host files.

All storage that support the `airfs.get_shareable_url` feature can be used as host.

Known list of supported storage:

* Amazon Web Services S3 (and compatible)
* Microsoft Azure Blobs Storage
* Microsoft Azure Files Storage
* OpenStack Swift / Object Store

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   getting_started
   api
   host_configuration
   changes

.. toctree::
   :maxdepth: 2
   :caption: Links

   airsd on GitHub <https://github.com/JGoutin/airsd>
   airsd on PyPI <https://pypi.org/project/airsd>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
