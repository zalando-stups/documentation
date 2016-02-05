.. _pierone:

========
Pier One
========

**Pier One** is STUPS' Docker registry with immutable tags, repo permissions, S3 backend and OAuth 2.0. It differs from
the public registry in that all tags and images are immutable which are required for reproducible deployments and for
internal and external audits. In addition, Pier One respects the notion of teams and allows access to namespaces based
on your team.

How to use it
=============

Pier One is fully Docker compliant. You can push Docker images using the normal Docker command line client:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-pierone
    $ pierone login # configures ~/.dockercfg
    $ docker build -t pierone.stups.example.com/your-team-id/myapp:0.1 .
    $ docker push pierone.stups.example.com/your-team-id/myapp:0.1

**How can I delete Docker images?**
    Docker images cannot be deleted as Pier One tries to ensure immutable deployment artifacts for audit compliance.

You can use the "-SNAPSHOT" tag suffix for mutable test artifacts:

.. code-block:: bash

    $ docker tag first-image-id pierone.stups.example.org/teamid/myapp:0.1-SNAPSHOT
    $ docker push pierone.stups.example.org/teamid/myapp:0.1-SNAPSHOT
    $ # now let's point our tag to some other image..
    $ docker tag some-other-image-id pierone.stups.example.org/teamid/myapp:0.1-SNAPSHOT
    $ docker push pierone.stups.example.org/teamid/myapp:0.1-SNAPSHOT # works!

Command Line Client
===================

Pier One comes with a convenience command line client:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-pierone
    $ pierone login # configures ~/.dockercfg

For example, you can list all your team artifacts:

.. code-block:: bash

    $ pierone artifacts myteam

You can use the ``latest`` command to see the latest (by creation time) tag for a given artifact:

.. code-block:: bash

    $ pierone latest myteam myapp
    1.8.5


How to configure
================

* Linux:

.. code-block:: bash

    $ cat ~/.config/pierone.yaml

* Mac:

.. code-block:: bash

    $ cat ~/Library/Application\ Support/pierone/pierone.yaml


Installation
============

See the :ref:`STUPS Installation Guide section on Pier One <pierone-deploy>` for details about deploying Pier One into your AWS account.
