.. _service-deployments:

===================
Service Deployments
===================

How to deploy the STUPS infrastructure service components.

.. Note::

    We will assume you are using a dedicated AWS account for the STUPS infrastructure components with the hosted zone **stups.example.org**.
    You may also deploy the STUPS infrastructure components into different accounts; please change the URLs according to your setup.

You will need the STUPS and AWS command line tools in order to install the STUPS infrastructure services:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups awscli

OAuth2 Provider
===============

Setting up the OAuth2 provider is highly vendor specific, please refer to your OAuth2 provider's manual.

We provide a `mock OAuth2 authorization server`_.


Token Service
=============

The **Token Service** is a proxy to allow getting OAuth2 access tokens without client credentials.

TODO

We provide a simple `mock Token Service`_.

Try out the Token Service with :ref:`zign`:

.. code-block:: bash

    $ zign token

Team Service
============

The **Team Service** allows getting team membership information. This is used by various components to restrict access to the user's own team(s).

We provide a simple `mock Team Service`_.

Try out the Team Service with curl:

.. code-block:: bash

    $ tok=$(zign token uid)
    $ curl -H "Authorization: Bearer $tok" https://team-service.stups.example.org/teams
    [{..}, ..]
    $ curl -H "Authorization: Bearer $tok" https://team-service.stups.example.org/user/jdoe
    [{..}, ..]

User Service
============

The **User Service** acts as a SSH public key provider for the "even" SSH access granting service.

You can setup your own SSH public key provider by running a HTTP service which allows downloading OpenSSH public keys (suitably formatted for the ``authorized_keys`` file)
by a simple GET request to an URL containing the user's ID (e.g. ``/users/{user}/ssh``).

Try out the SSH public key endpoint with an existing user:

.. code-block:: bash

    $ tok=$(zign token uid)
    $ curl -H "Authorization: Bearer $tok" https://user-service.stups.example.org/employees/jdoe/ssh
    ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAA..


.. _even-deploy:

even
====

The **even** service allows getting SSH access to any team server.

Create a new internal PostgreSQL cluster in RDS and create the "even" database.

Create the necessary security groups and IAM role by running "senza init":

.. code-block:: bash

    $ senza init even.yaml # we will overwrite even.yaml later anyway


Copy example Senza definition YAML and change the URLs to point to your IAM services.

.. code-block:: bash

    $ wget -O even.yaml https://raw.githubusercontent.com/zalando-stups/even/master/example-senza-definition.yaml
    $ vim even.yaml

Create a new KMS key for "even" and give the ``app-even`` IAM role permissions to use the KMS key.
Encrypt the private SSH key of the "granting-service" Taupage user with KMS and put the cipher text (prefixed with "aws:kms:") into ``even.yaml``.

.. code-block:: bash

    $ privkey=$(cat ~/.ssh/ssh-access-granting-service) # use the key generated when building Taupage
    $ aws kms encrypt --key-id 123 --plaintext "$privkey" # encrypt with KMS

Deploy.

.. code-block:: bash

    $ senza create even.yaml 1 $LATEST_VER

Try out the SSH granting service with :ref:`piu`.

.. _pierone-deploy:

Pier One
========
**Pier One** is STUPS' Docker registry.

Create a new S3 bucket (e.g. ``exampleorg-stups-pierone-eu-west-1``) to store the Docker images in.

Create a new internal PostgreSQL cluster in RDS with its own ``app-pierone-db`` security group and create the "pierone" database.

Create the necessary security groups and IAM role by running "senza init":

.. code-block:: bash

    $ senza init pierone.yaml # we will overwrite pierone.yaml later anyway

Give the ``app-pierone`` security access to the RDS database (``app-pierone-db`` security group).

Copy the example Senza definition YAML and change the bucket name and DB_SUBNAME.

.. code-block:: bash

    $ wget -O pierone.yaml https://raw.githubusercontent.com/zalando-stups/pierone/master/example-senza-definition.yaml
    $ vim pierone.yaml


Give the IAM role ``app-pierone`` write access to your S3 bucket. The IAM policy might look like:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowStoringDockerImages",
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:PutObject"
                ],
                "Resource": [
                    "arn:aws:s3:::exampleorg-stups-pierone-eu-west-1",
                    "arn:aws:s3:::exampleorg-stups-pierone-eu-west-1/*"
                ]
            }
        ]
    }

Deploy.

.. code-block:: bash

    $ senza create pierone.yaml 1 $LATEST_VER

Try pushing a Docker image.

.. code-block:: bash

    $ pierone login
    $ docker pull busybox
    $ docker tag busybox pierone.stups.example.org/myteam/busybox:0.1
    $ docker push pierone.stups.example.org/myteam/busybox:0.1


.. _kio-deploy:

Kio
===
**Kio** is STUPS' application registry.

Create a new internal PostgreSQL cluster in RDS and create the "kio" database.

Copy the example Senza definition YAML and change the DB_SUBNAME and URLs.

.. code-block:: bash

    $ wget -O kio.yaml https://raw.githubusercontent.com/zalando-stups/kio/master/example-senza-definition.yaml
    $ vim kio.yaml

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

**YOUR TURN** is STUPS' developer console. It is a pure Javascript application including a very small backend. Currently it depends on the following STUPS services:

* Kio
* Twintip
* mint
* essentials
* Pier One
* fullstop.

You also need:

* an IAM solution that issues OAuth2 access tokens
* a team service

(See also the STUPS mocks for these.)

Copy the example Senza definition YAML and change the environment variables accordingly.

.. code-block:: bash

    $ wget -O yourturn.yaml https://raw.githubusercontent.com/zalando-stups/yourturn/master/example-senza.yaml
    $ vim yourturn.yaml

fullstop.
=========
TODO


.. _mock OAuth2 authorization server: https://github.com/zalando-stups/mocks/tree/master/oauth2-provider
.. _mock Token Service: https://github.com/zalando-stups/mocks/tree/master/token-service
.. _mock Team Service: https://github.com/zalando-stups/mocks/tree/master/team-service
