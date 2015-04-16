.. _mai:

===
Mai
===

**Mai** is a command line utility to retrieve temporary AWS credentials.

How to use
==========

Creating a new profile:

.. code-block:: bash

    $ mai create myteam
    # answer the questions


If you only have one profile, you can simply execute ``mai`` to login:

.. code-block:: bash

    $ mai
    $ # credentials are now stored in ~/.aws/credentials
    $ aws ec2 describe-instances # example usage

.. Note:: Mai will save its configuration in a YAML file in your home directory (``~/.config/mai/mai.yaml`` on Linux)
