.. _`account configuration`:

=====================
Account Configuration
=====================

AWS accounts are configured by the :ref:`sevenseconds` command line tool.

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-sevenseconds

Seven Seconds can update all AWS team accounts one after each other:

.. code-block:: bash

    $ sevenseconds configure --saml-user jdoe@example.org configuration.yaml '*'
