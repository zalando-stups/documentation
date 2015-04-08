==========
Deployment
==========

The :ref:`senza` command line tools allows deploying application stacks.

.. code-block:: bash

    $ pip3 install --upgrade stups-mai stups-senza

First deploy the application's artifact (Docker image) to :ref:`pierone`, e.g.:

.. code-block:: bash

    $ cd myapp # enter your application's source folder
    $ docker build -t pierone.stups.example.org/myteam/myapp:1.0 .
    $ docker push pierone.stups.example.org/myteam/myapp:1.0

Next you need to create a new deployment definition YAML file:

.. code-block:: yaml

    SenzaInfo:
    SenzaComponents:


In order to create the Cloud Formation stack, we need to login with :ref:`mai`:

.. code-block:: bash

    $ mai create myteam # create a new profile (if you haven't done so)
    $ mai # login

Create the application's Cloud Formation stack with Senza:

.. code-block:: bash

    $ senza create definition.yaml 1 1.0
