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

Generate a new SSH keypair to be used for the "granting-service" user.
Store the private SSH key in a safe place (you will need it later for deploying the "even" SSH access granting service, see :ref:`how to deploy even <even-deploy>`).
Copy the public SSH key into ``my-taupage-config/secret/ssh-access-granting-service.pub``.

Edit the example configuration files as needed:

.. code-block:: bash

    $ vim my-taupage-config/config-stups.sh
    $ # edit my-taupage-config/secret/* files


Build a new Taupage AMI:

.. code-block:: bash

    $ cd taupage
    $ ./create-ami.sh ../my-taupage-config/config-stups.sh
