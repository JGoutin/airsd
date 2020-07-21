Getting Started
===============

Installation
------------

Supported Python versions: >= 3.6

Installation is performed using PIP:

.. code-block:: bash

    pip install airsd

All mandatory dependencies are automatically installed.
You can also install these optional extras:

* ``all``: Install all extras.
* ``s3``: Amazon Web Services S3 support.

Example of installing airsd with all dependencies:

.. code-block:: bash

    pip install airsd[all]

Example for installing with support only for S3:

.. code-block:: bash

    pip install airsd[s3]

Usage
-----



Storage configuration
---------------------

Advanced configuration
~~~~~~~~~~~~~~~~~~~~~~

storage side configuration file (Sender requires read access)

airsd storage root path may be in a sub-directory

* files directory (Sender require read and write access)
* random prefix (default: true)
* Max expiry (indicative, only raise error client side)

Files lifecycle
~~~~~~~~~~~~~~~

Advanced user configuration
---------------------------

User configuration file

* default storage (Default to latest used if not specified)
* compression (default gz)
