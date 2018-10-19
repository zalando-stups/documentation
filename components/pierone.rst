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
    $ pierone login # configures ~/.docker/config.json
    $ docker build -t pierone.stups.example.com/your-team-id/myapp:0.1 .
    $ docker push pierone.stups.example.com/your-team-id/myapp:0.1

**How can I delete Docker images?**
    Docker images cannot be deleted as Pier One tries to ensure immutable deployment artifacts for audit compliance.

Permissions
===========

Pier One allows you to push Docker images based on team permissions.
Pushing to "pierone.stups.example.org/myteam/myapp:1.0" is allowed if at least one of the following is true:

* You are pushing with your own user (employee) credentials and you belong to the team "myteam".
* A service user (application registered in Kio) is pushing and the OAuth token has the "application.write" scope and the service user (application) is assigned to the team "myteam".
* A service user is pushing and the OAuth token has the "application.write_all" scope.

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
----------------

The command line client uses the OS' default configuration location.

Linux:

.. code-block:: bash

    $ cat ~/.config/pierone.yaml

Mac:

.. code-block:: bash

    $ cat ~/Library/Application\ Support/pierone/pierone.yaml


Using the CLI for Service Users
-------------------------------

The Pier One command line client automatically tries to use "service" tokens if
the right environment variables are set:

``OAUTH2_ACCESS_TOKEN_URL``
    URL of the OAuth2 token endpoint, e.g. https://token.services.example.org/oauth2/access_token
``CREDENTIALS_DIR``
    Path to the OAuth2 service user credentials (``user.json`` and ``client.json``)

See the `Python tokens library`_ for more information.

The service user needs to have the "application.write" scope granted.
You can assign the "application.write" scope to the service user (e.g. CI/CD application) in :ref:`yourturn`.

Example how the CLI can be used in a CI/CD build pipeline:

.. code-block:: bash

    # OAUTH2_ACCESS_TOKEN_URL must point to the correct OAuth2 token endpoint for service users
    export OAUTH2_ACCESS_TOKEN_URL=https://token.services.example.org/oauth2/access_token
    # NOTE: CREDENTIALS_DIR is already automatically set by the Taupage AMI
    export CREDENTIALS_DIR=/meta/credentials
    pierone login --url pierone.example.org  # will write ~/.docker/config.json
    # pushing to the "myteam" repo will only work if "myteam" is assigned to the service user (application)
    docker push pierone.example.org/myteam/myartifact:cd${BUILD_NUMBER}


Installation
============

See the :ref:`STUPS Installation Guide section on Pier One <pierone-deploy>` for details about deploying Pier One into your AWS account.

.. _Python tokens library: https://github.com/zalando-stups/python-tokens
