.. _kio:

===
Kio
===

**Kio** is STUPS' application registry. Kio holds all basic information about **applications**.

Most services of STUPS rely on Kio for being the authoritative source for existing applications. Before you deploy an
application in the STUPS infrastructure, you have to register it in Kio. You can use :ref:`yourturn` to have a nice UI
on top of Kio or you can access it via command line tool or the `REST API`_.

Registered applications are automatically crawled for their API definitions by :ref:`twintip` and get service users in
your IAM solution by :ref:`mint`.

Command Line Client
===================

Kio comes with a convenience command line client:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups
    $ stups configure # will configure Kio URL too

For example, you can list all applications, that are owner by a certain team:

.. code-block:: bash

    $ kio app list --team myteam
    
You can view the details of one app:

.. code-block:: bash

    $ kio app show myapp

You can also update properties of apps:

.. code-block:: bash

    $ kio app update myapp active=false

Installation
============

See the :ref:`STUPS Installation Guide section on Kio <kio-deploy>` for details about deploying the Kio application registry into your AWS account.

.. _REST API: https://github.com/zalando-stups/kio/blob/master/resources/api/kio-api.yaml
