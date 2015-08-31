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

You can either use Homebrew or MacPorts to install Python 3.4 on Mac OS X.

Install Python 3 using Homebrew (pip3 already comes with this package)

.. code-block:: bash

    $ brew install python3

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
