.. _taupage-ami-creation:

====================
Taupage AMI Creation
====================

How to build a new private :ref:`taupage` AMI.

.. code-block:: bash

    $ git clone git@github.com:zalando-stups/taupage.git
    $ mkdir my-taupage-config
    $ cp -r taupage/secret my-taupage-config
    $ cp taupage/config-stups-example.sh my-taupage-config/config-stups.sh

Edit the example configuration files as needed:

.. code-block:: bash

    $ vim my-taupage-config/config-stups.sh
    $ # edit my-taupage-config/secret/* files

Build a new Taupage AMI:

.. code-block:: bash

    $ cd taupage
    $ ./create-ami.sh ../my-taupage-config/config-stups.sh
