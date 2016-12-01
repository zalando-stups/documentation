.. _local-setup:

===========
Local Setup
===========

This section describes how to set up your local machine to use the STUPS tools.

In general you will need:

* Python 3.4+
* Docker 1.11+

Linux
=====

Python 3 is usually already installed on Ubuntu.
You will need the PIP package manager to install STUPS tools:

.. code-block:: bash

    $ sudo apt-get install python3-pip

Install Docker on Ubuntu according to the `Docker on Ubuntu installation instructions`_.

Install the aws-cli

.. code-block:: bash

    $ sudo pip3 install --upgrade awscli

Check that everything works by running:

.. code-block:: bash

    $ python3 --version  # should print Python 3.4.0 (or higher)
    $ docker info        # should work without using sudo!


Mac
===

Local Environment
-----------------

OS X users may need to set their locale environment to UTF-8::

    # You can put these two commands in your local shell initialization script
    # e.g. ~/.bashrc or ~/.zshrc
    export LC_ALL=en_US.utf-8
    export LANG=en_US.utf-8

Install Python and Docker
-------------------------

You can either use Homebrew or :ref:`local-setup-macports` to install Python 3.4 on Mac OS X.

Install Python 3 using Homebrew (pip3 already comes with this package)

.. code-block:: bash

    $ brew install python3

Install Docker on Mac according to the `Docker on Mac installation instructions`_, then install the aws commandline tool.

.. code-block:: bash

    $ brew install awscli

Check that everything works by running:

.. code-block:: bash

    $ python3 --version  # should print Python 3.4.0 (or higher)
    $ docker info        # should work without using sudo!

.. _Docker on Ubuntu installation instructions: http://docs.docker.com/installation/ubuntulinux/
.. _Docker on Mac installation instructions: http://docs.docker.com/installation/mac/
