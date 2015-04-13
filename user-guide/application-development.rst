=======================
Application Development
=======================

To be written...

* Applications should be developed as microservices which focus on small tasks.
* Applications should follow the `Twelve-Factor App Principle`_.
* Application APIs shoud be RESTful
* Applications must be deployed as Docker artifacts


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

An example implementation on how to generate the ``scm-source.json`` file with Bash:

.. code-block:: bash

    #!/bin/bash
    REV=$(git rev-parse HEAD)
    URL=$(git config --get remote.origin.url)
    STATUS=$(git status --porcelain)
    if [ -n "$STATUS" ]; then
        REV="$REV (locally modified)"
    fi
    # finally write hand-crafted JSON to scm-source.json
    echo '{"url": "git:'$URL'", "revision": "'$REV'", "author": "'$USER'", "status": "'$STATUS'"}' > scm-source.json

Logging
=======

Applications should log to STDOUT. The runtime environment (:ref:`Taupage`) will do appropriate log shipping to a central log UI provider.
Application logs must not contain any personal and/or sensitive information such as customer data, credentials or similar.


.. _Twelve-Factor App Principle: http://12factor.net/
.. _Zalando Ubuntu Docker base image: https://registry.hub.docker.com/u/zalando/ubuntu/
.. _Zalando OpenJDK Docker base image: https://registry.hub.docker.com/u/zalando/openjdk/
