===========
Walkthrough
===========

.. Caution::

    This walkthrough is **work in progress**!


This walkthrough should show all steps for one sample application from birth to death.
Please see the other sections in the User's Guide for more information about specific topics.

Install STUPS command line tools.

.. code-block:: bash

    $ sudo pip3 install --upgrade stups

Build the sample artifact.

.. code-block:: bash

    $ docker build -t pierone.stups.example.org/myteam/sample:0.1 .

Push to Pier One.

.. code-block:: bash

    $ pierone login
    $ docker push pierone.stups.example.org/myteam/sample:0.1

Find out your mint bucket.

.. code-block:: bash

    $ aws s3 # TODO

Register your app in Kio, remember your app ID.

Configure your app's mint bucket.

This will trigger the mint worker to write your app credentials to your mint bucket.

Create a new Senza definition by doing senza init.

.. code-block:: bash

    $ senza init sample.yaml

Enter your app ID and mint bucket.

Add your Scalyr account key.

Create your stack.

.. code-block:: bash

    $ senza create sample.yaml

Senza will generate CF JSON
CF stack is created
ASG launches Taupage instance
Taupage starts Scalyr agent
Taupage runs berry to download app credentials
Taupage pushes Taupage config userdata to fullstop.
Taupage pulls Docker image from Pier One using the app credentials
Taupage starts the Docker container
Taupage signals CFN
Wait for completion.

.. code-block:: bash

    $ senza status sample.yaml -w 2

Test stack.

.. code-block:: bash

    $ curl -v https://sample-1.myteam.example.org/

Route traffic to your new stack.

.. code-block:: bash

    $ senza traffic sample 1 100

Shut down the stack.

.. code-block:: bash

    $ senza del sample 1
