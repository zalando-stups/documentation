.. _piu:

===
Più
===

**Più** is the command line client for the :ref:`even` SSH access granting service.

Installation
============

Install or upgrade to the latest version of Più (|piu-pypi-version|) with PIP:

.. |piu-pypi-version| image:: https://img.shields.io/pypi/v/stups-piu.svg
   :target: https://pypi.python.org/pypi/stups-piu/
   :alt: Latest PyPI version

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-piu

How to use
==========

See the section :ref:`ssh-access` on how to get SSH access to EC2 instances with Più.

How to configure
================

* Linux:

.. code-block:: bash

    $ cat ~/.config/piu.yaml

* Mac:

.. code-block:: bash

    $ cat ~/Library/Application\ Support/piu/piu.yaml

An example configuration:

.. code-block:: json

    {even_url: 'https://even.example.com', odd_host: 'odd-eu-west-1.example.com'}

