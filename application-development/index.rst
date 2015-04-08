=======================
Application Development
=======================

To be written...

* Applications should be developed as microservices which focus on small tasks.
* Applications should follow the `Twelve-Factor App Principle`_.
* Application APIs shoud be RESTful
* Applications should be deployed as Docker artifacts


Docker
======

* Use the existing Zalando Ubuntu base images which already include the Zalando CA:

  * `Zalando Ubuntu Docker base image`_
  * `Zalando OpenJDK Docker base image`_

* Use Docker environment variables (``-e KEY=val``) for static configuration (e.g. database connection)
* Log to STDOUT and rely on the host system to do log shipping
* Do not mutate Docker tags, i.e. treat all Docker tags ("versions") as immutable and always push a new tag for a new application version (immutable tags might be enforced in the registry in the future)

The final application deployment artifact (Docker image) must contain a ``scm-source.json`` file in the root directory.
This meta file is in JSON format and must reference the SCM source location the Docker image was built from.
The JSON file should contain a single JSON dictionary with the following keys:

``url``
    The SCM URL in the format ``<SCM-PROVIDER>:<PROVIDER-SPECIFIC-REPO-LOCATION>``.
``revision``
    The SCM revision, e.g. the full git commit sha1.
    The revision should end with the marker text " (locally modified)" for unclean working directories.
    This marker text ensures that no exact match for such revisions can be found in the remote SCM repository.
``author``
    Name of the file's author. The author is responsible for the correctness of the file's contents.
``status``
    Optional SCM working directory status information. Might contain ``git status`` output for example.

Example:

.. code-block:: json

    {
    "url": "git:git@github.com:zalando/bastion-host.git",
    "revision": "cd768599e1bb41c38279c26254feff5cf57bf967",
    "author": "hjacobs",
    "status": ""
    }


Troubleshooting
===============

To ease troubleshooting problems, EC2 instances can be accessed via SSH using the account's **SSH Bastion Host**.
SSH access to the bastion host and the internal EC2 instance (internal EC2 instances are using the private IP range 172.31.0.0/16)
can be requested via the **SSH Access Granting Service**. A convenience script is provided in the ``bin`` directory. Usage:

.. code-block:: bash

    $ git clone https://github.com/zalando/ssh-access-granting-service
    $ export PATH=$PATH:$(pwd)/ssh-access-granting-service/bin
    $ # assumptions: region is Frankfurt, team name is "myteam", private EC2 instance has IP "172.31.146.1"
    $ ssh-request bastion-eu-central-1.myteam.example.org -r 172.31.146.1 "Troubleshoot problem XY"
    $ ssh -A bastion-eu-central-1.myteam.example.org # agent-forwarding must be used!
    $ ssh 172.31.146.1 # jump from bastion to private instance



.. _Twelve-Factor App Principle: http://12factor.net/
.. _Zalando Ubuntu Docker base image: https://registry.hub.docker.com/u/zalando/ubuntu/
.. _Zalando OpenJDK Docker base image: https://registry.hub.docker.com/u/zalando/openjdk/
