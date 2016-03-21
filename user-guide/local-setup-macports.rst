.. _local-setup-macports:

===============================
Installing Python with MacPorts
===============================

Using MacPorts things are a little different. First check if you have the correct Python version installed.

.. code-block:: bash

    $ port select --list python
    Available versions for python:
        python26-apple
        python27 (active)
        python27-apple

This output demonstrates you don't have the correct version so do a:

.. code-block:: bash

    $ port install python34

Next you want to set the correct default version:

.. code-block:: bash

    $ port select --set python python34
    Selecting 'python34' for 'python' succeeded. 'python34' is now active.

In order to get pip up and running download and set pip as well:

.. code-block:: bash

    $ port install py34-pip
    $ port select --list pip
    Available versions for pip:
        none
        pip27 (active)
        pip34
    $ port select --set pip pip34
    Selecting 'pip34' for 'pip' succeeded. 'pip34' is now active.

Nearly there. Now set the correct path since MacPorts does not install python3 under /usr/local. But thats simple:

.. code-block:: bash

    $ which python
    /opt/local/bin/python
    $ which python3
    ''
    $ export PATH=/opt/local/Library/Frameworks/Python.framework/Versions/3.4/bin:$PATH
    $which python3
    /opt/local/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

That should do it.
