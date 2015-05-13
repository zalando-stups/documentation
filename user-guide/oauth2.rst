.. _oauth2:

=====
OAuth
=====

STUPS services are generally secured via OAuth 2. Services automatically get OAuth credentials via :ref:`mint` & :ref:`berry`, but human users need to either use the implicit flow for web UIs (redirect) or they need to retrieve an access token on the command line via :ref:`zign`.

Install :ref:`zign` command line tool to generate OAuth 2 access tokens:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-zign


.. code-block:: bash

    $ zign token uid # get access token with "uid" scope

You can name tokens and retrieve them later programmatically:

.. code-block:: bash

    $ zign token -n testing uid
    $ zign list -o json

