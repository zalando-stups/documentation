.. _local-setup:

===========
Local Setup
===========

This section describes how to set up your local machine to use the STUPS tools.

In general you will need:

* Python 3.4
* Docker 1.7+

Linux
=====

Python 3 is usually already installed on Ubuntu.
You will need the PIP package manager to install STUPS tools:

.. code-block:: bash

    $ sudo apt-get install python3-pip

Install Docker on Ubuntu according to the `Docker on Ubuntu installation instructions`_.

Check that everything works by running:

.. code-block:: bash

    $ python3 --version  # should print Python 3.4.0 (or higher)
    $ docker info        # should work without using sudo!


Mac
===

Local Environment
-----------------

OS X users may need to set their locale environment to UTF-8 with::

    export LC_ALL=en_US.utf-8
    export LANG=en_US.utf-8

You can either use Homebrew or MacPorts to install Python 3.4 on Mac OS X.

Homebrew
--------

=======
You can either use Homebrew or MacPorts to install Python 3.4 on Mac OS X.

Install Python 3 using Homebrew (pip3 already comes with this package)

.. code-block:: bash

    $ brew install python3


You can put these two commands in your local shell initialization script, e.g. ``.bashrc``.

MacPorts
--------

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

Docker
------
=======
OS X users may need to set their locale environment to UTF-8 with::

    export LC_ALL=en_US.utf-8
    export LANG=en_US.utf-8

You can put these two commands in your local shell initialization script, e.g. ``.bashrc``.

Install Docker on Mac according to the `Docker on Mac installation instructions`_.

Check that everything works by running:

.. code-block:: bash

    $ python3 --version  # should print Python 3.4.0 (or higher)
    $ docker info        # should work without using sudo!

.. _Docker on Ubuntu installation instructions: http://docs.docker.com/installation/ubuntulinux/
.. _Docker on Mac installation instructions: http://docs.docker.com/installation/mac/
