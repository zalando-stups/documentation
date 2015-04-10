.. _pierone:

========
Pier One
========

**Pier One** is STUPS' Docker registry with immutable tags, repo permissions, S3 backend and OAuth.

You can push Docker images to Pier One using the Docker command line client:

.. code-block:: bash

    $ # replace "teamid" with your team's ID
    $ docker tag EXISTING-IMAGE-ID pierone.stups.example.org/teamid/myapp:0.1
    $ docker push pierone.stups.example.org/teamid/myapp:0.1

**How can I delete Docker images?**
    Docker images cannot be deleted as Pier One tries to ensure immutable deployment artifacts for audit compliance.

You can use the "-SNAPSHOT" tag suffix for mutable test artifacts:

.. code-block:: bash

    $ docker tag first-image-id pierone.stups.example.org/teamid/myapp:0.1-SNAPSHOT
    $ docker push pierone.stups.example.org/teamid/myapp:0.1-SNAPSHOT
    $ # now let's point our tag to some other image..
    $ docker tag some-other-image-id pierone.stups.example.org/teamid/myapp:0.1-SNAPSHOT
    $ docker push pierone.stups.example.org/teamid/myapp:0.1-SNAPSHOT # works!
