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
    $ Identity provider URL: https://aws.example.org # Enter your Identity Provider URL 
    $ SAML username: john.doe@example.org # Enter your SAML username
    # answer the questions

Deleting a profile:

.. code-block:: bash

    $ mai delete myteam
    
List profile(s):

.. code-block:: bash

    $ mai list

If you only have one profile, you can simply execute ``mai`` to login:

.. code-block:: bash

    $ mai
    $ # credentials are now stored in ~/.aws/credentials
    $ aws ec2 describe-instances # example usage

.. Note:: Mai will save its configuration in a YAML file in your home directory (``~/.config/mai/mai.yaml`` on Linux, ``~/Library/Application\ Support/mai/mai.yaml`` on OSX)
