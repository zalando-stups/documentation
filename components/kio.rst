.. _kio:

===
Kio
===

**Kio** is STUPS' application registry. Kio holds all basic information about **applications**, **application versions**
and **approvals**.

Most services of STUPS rely on Kio for being the authoritative source for existing applications. Before you deploy an
application in the STUPS infrastructure, you have to register it in Kio. You can use :ref:`yourturn` to have a nice UI
on top of Kio or you can access it via its `REST API`_.

Registered applications are automatically crawled for their API definitions by :ref:`twintip` and get service users in
your IAM solution by :ref:`mint`.

Application Versions and Approvals
==================================

In order to be compliant with internal and external audits, we need to track application versions as an abstract
construct which is connected with deployment artifacts and human approvals.

If you deploy a new version of your software in STUPS, you have to create a new version in Kio and provide some basic
information. Mainly the deployment artifact that corresponds to your version.

Depending on the criticality of your software, you might need to get certain approvals that have to be added to Kio.
:ref:`fullstop` will regularly check your servers and your data in Kio and report violations.
Kio will delete approvals for a version when you update it.

All those steps can be done in :ref:`fullstop` for humans or via REST APIs.

Command Line Client
===================

Kio comes with a convenience command line client:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups
    $ stups configure # will configure Kio URL too

For example, you can list all your app versions:

.. code-block:: bash

    $ kio ver li myapp

You can also create and approve new application versions:

.. code-block:: bash

    $ kio ver create myapp 1.0 docker://pierone.example.org/myteam/myapp:1.0
    $ kio ver approve myapp 1.0

Installation
============

See the :ref:`STUPS Installation Guide section on Kio <kio-deploy>` for details about deploying the Kio application registry into your AWS account.

.. _REST API: https://github.com/zalando-stups/kio/blob/master/resources/api/kio-api.yaml
