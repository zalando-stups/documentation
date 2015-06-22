===========
Walkthrough
===========

.. Caution::

    This walkthrough is **work in progress**!


This walkthrough should show all steps for one sample application from birth to death.
Please see the other sections in the :ref:`user-guide` for more information about specific topics.

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

    $ aws s3 ls | grep mint
    2015-06-17 12:14:27 exampleorg-stups-mint-123456789123-eu-west-1

Register your app in Kio by using the YOUR TURN developer console in your browser ("yourturn.stups.example.org").
Remember your application ID (we use "sample" here).

Configure your application's mint bucket (click on the "Access Control" button on your app's page in YOUR TURN).

This will trigger the mint worker to write your app credentials to your mint bucket.
Wait for the first credentials to appear:

.. code-block:: bash

    $ aws s3 ls s3://exampleorg-stups-mint-123456789123-eu-west-1
    # there should be a new folder for your application


Create a new Senza definition by doing senza init.

.. code-block:: bash

    $ senza init sample.yaml

Choose the "webapp" template. Enter your application ID "sample" and mint bucket "exampleorg-stups-mint-123456789123-eu-west-1".

Lookup your Scalyr account key in the Scalyr web UI.
Add the Scalyr account key into the Senza definition YAML file.

Create your stack.

.. code-block:: bash

    $ senza create sample.yaml

* Senza will generate CF JSON
* CF stack is created
* ASG launches Taupage instance
* Taupage starts Scalyr agent
* Taupage runs berry to download app credentials
* Taupage pushes Taupage config userdata to fullstop.
* Taupage pulls Docker image from Pier One using the app credentials
* Taupage starts the Docker container
* Taupage signals CFN

Wait for completion by watching the Senza status output.

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
