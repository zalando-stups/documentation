.. _zign:

====
Zign
====

**Zign** is the command line client to generate OAuth2 access tokens.

Installation
============

Install or upgrade to the latest version of Zign (|zign-pypi-version|) with PIP:

.. |zign-pypi-version| image:: https://img.shields.io/pypi/v/stups-zign.svg
   :target: https://pypi.python.org/pypi/stups-zign/
   :alt: Latest PyPI version

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-zign

How to use
==========

See the section :ref:`access-control-helpful-tooling` on how to retrieve access tokens with Zign.

Configuration
=============

Zign stores its configuration in a YAML file in your home directory (``~/.config/zign/zign.yaml`` on Linux, ``~/Library/Application\ Support/zign/zign.yaml`` on OSX).

The minimal configuration contains the Token Service URL:

.. code-block:: yaml

    {url: 'https://token.example.org/access_token'}

Zign uses the ``USER`` and ``ZIGN_USER`` environment variables to determine the username to use.
You might want to overwrite this in the configuration file:

.. code-block:: yaml

    {
        url: 'https://token.example.org/access_token',
        user: 'jdoe'
    }

