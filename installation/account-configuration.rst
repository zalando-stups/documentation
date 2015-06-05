.. _`account configuration`:

=====================
Account Configuration
=====================

AWS accounts are configured by the :ref:`sevenseconds` command line tool.

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-sevenseconds

Minimal Account Configuration
=============================

First you need to put your root access key credentials into ``~/.aws/credentials`` for initial account configuration.

Next copy the minimal example configuration file to a new location and edit it:

.. code-block:: bash

    $ git clone git@github.com:zalando-stups/sevenseconds.git
    $ cp sevenseconds/examples/example-minimal-configuration.yaml myconfig.yaml
    $ vim myconfig.yaml


Now run Seven Seconds on your new AWS account:

.. code-block:: bash

    $ sevenseconds configure myconfig.yaml myaccount




Configuring Multiple Accounts
=============================

Seven Seconds can update all AWS team accounts one after each other:

.. code-block:: bash

    $ sevenseconds configure --saml-user jdoe@example.org configuration.yaml '*'
