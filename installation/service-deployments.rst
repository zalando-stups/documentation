===================
Service Deployments
===================

How to deploy the STUPS infrastructure service components.

.. Note::

    We will assume you are using a dedicated AWS account for the STUPS infrastructure components with the hosted zone **stups.example.org**.
    You may also deploy the STUPS infrastructure components into different accounts; please change the URLs according to your setup.

OAuth2 Provider
===============

Setting up the OAuth2 provider is highly vendor specific, please refer to your OAuth2 provider's manual.

We provide a mock to use as OAuth2 authorization server: https://github.com/zalando-stups/mocks/tree/master/oauth2-provider

Token Service
=============

The Token Service is a proxy to allow getting OAuth2 access tokens without client credentials.

TODO

We provide a simple mock to use as Token Service: https://github.com/zalando-stups/mocks/tree/master/token-service

Try out the Token Service with :ref:`zign`:

.. code-block:: bash

    $ zign token

Team Service
============

The Team Service allows getting team membership information. This is used by various components to restrict access to the user's own team(s).

TODO

We provide a simple mock to use as Team Service: https://github.com/zalando-stups/mocks/tree/master/team-service

User Service
============

The User Service acts as a SSH public key provider.

You can setup your own SSH public key provider by running a HTTP service which allows downloading OpenSSH public keys (suitably formatted for the ``authorized_keys`` file)
by a simple GET request to an URL containing the user's ID (e.g. ``/users/{user}/ssh``).

even
====

The **even** service allows getting SSH access to any team server.

Create a new PostgreSQL cluster in RDS and create the "even" database.

Encrypt the private SSH key with KMS.
Copy example Senza definition YAML and change the URLs to point to your IAM services.
Deploy.

Try out the SSH granting service with :ref:`piu`.

Pier One
========
Create a new S3 bucket.
Create a new PostgreSQL cluster in RDS and create the "pierone" database.
Copy the example Senza definition YAML and change the bucket name and DB_SUBNAME.
Give the IAM role write access to your S3 bucket.
Deploy.
Try pushing a Docker image.

.. code-block:: bash

    $ pierone login
    $ docker pull busybox
    $ docker tag busybox pierone.stups.example.org/myteam/busybox:0.1
    $ docker push pierone.stups.example.org/myteam/busybox:0.1


Kio
===

TODO

essentials
==========

TODO

mint Storage
============

TODO

mint Worker
===========

TODO

YOUR TURN
==========

TODO

fullstop.
=========
TODO

