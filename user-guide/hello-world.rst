===========
Hello world
===========

.. Important::

    Please read :ref:`local-setup` to make sure you installed Python and Docker correctly.

    Some hints:

    .. code-block:: bash

        * docker - 1.9
        * python 3 (export LC_ALL=en_US.utf-8 export LANG=en_US.utf-8)
        * sudo pip3 install -U stups -> will install all stups cli tools
            * this will not include zmon ( sudo pip3 install --upgrade zmon-cli )


This guide should show all steps for one sample application from birth to death.
Please see the other sections in the :ref:`user-guide` for more information about specific topics.

Install STUPS command line tools and configure them.

.. code-block:: bash

    $ sudo pip3 install --upgrade stups
    $ stups configure

First of all clone this example project:

.. code-block:: bash

    $ git clone git@github.com:zalando-stups/zalando-cheat-sheet-generator.git

Create this new application in yourturn:

.. code-block:: bash

    https://yourturn.stups.example.org

Now you will need to create the ``scm-source.json`` file that refer your docker image to a specific git revision number.

Here more information :ref:`scm-source-json`.

.. code-block:: bash

    $ ./generate-scm-source-json.sh

Let's start the application and see if all works:

.. code-block:: bash

    $ python -m http.server 8000
    http://localhost:8000/index.html?schema=schema/stups.json

Nice! Let's build the docker images:

Build with the Dockerfile in the repo.

.. code-block:: bash

    $ docker build -t pierone.stups.example.org/<your-team>/zalando-cheat-sheet-generator:0.1 .

And now see if is listed locally:

.. code-block:: bash

    $ docker images

Let's also try if the docker images works!

.. code-block:: bash

    $ docker run -it pierone.stups.example.org/<your-team>/zalando-cheat-sheet-generator:0.1
    # and test with this url: http://localhost:8000/index.html?schema=schema/stups.json

If all works, we are ready to login in pierone and push it.

.. code-block:: bash

    $ pierone login
    $ docker push pierone.stups.example.org/<your-team>/zalando-cheat-sheet-generator:0.1

Let's check if we can find it in the pierone repository (login needed if your token expired):

.. code-block:: bash

    $ pierone login
    $ pierone tags <your-team> zalando-cheat-sheet-generator

Now let's create the version in yourturn for the application created:

.. code-block:: bash

    https://yourturn.stups.example.org

Configure your application's mint bucket (click on the "Access Control" button on your app's page in YOUR TURN).

This will trigger the mint worker to write your app credentials to your mint bucket.
Wait for the first credentials to appear:

.. code-block:: bash

    $ aws s3 ls s3://mint-example-bucket
    # there should be a new folder for your application

Deploy!

List aws account:

.. code-block:: bash

    $ mai list

Login via console to your aws account:

.. code-block:: bash

    $ mai login <account-name>

Create a senza definition file for that:

.. code-block:: bash

    $ senza init deploy-definition.yaml

* Choose the "webapp" template.
* Enter the application ID "zalando-cheat-sheet-generator"
* Enter the docker image "pierone.stups.example.org/<your-team>/zalando-cheat-sheet-generator"
* Enter the port "8000" (see the Dockerfile [why 8000?? no reason for that :D])
* Health check path is the default "/" (would obviously be better to have a specific one)
* Go for "t2.micro"
* Use the default mint bucket

.. Caution::
    Take the internal LB! We have no OAUTH2 configured!!!

* and let senza create the security group and IAM role for us.

After this, you can also add a log provider or other configuration,
if you like to encrypt your password check this :ref:`guide <key-encryption>`.

Create your stack.

.. code-block:: bash

    $ senza create deploy-definition.yaml 1 0.1

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

    $ senza status deploy-definition.yaml -w 2

or senza events:

.. code-block:: bash

    $ senza events deploy-definition.yaml 1 -w 2

.. Important::

    In case of error go to your log provider, if you did not configure it.
    Go in aws, EC2 service, find your instance, right click, Instance Settings, Get System Log

Test stack.

.. code-block:: bash

    $ curl -v http://<address>:8000/index.html?schema=schema/stups.json

.. Important::

    This will not works! Because of the missing OAUTH2 we have created an internal LB.
    To test it we will need to :ref:`follow the same guide as for a DB connection <dig-a-tunnel>` and than try again.

Get instance IP:

.. code-block:: bash

    $ senza instances zalando-cheat-sheet-generator

Let us piu to the Odd bation host:

.. code-block:: bash

    $ piu odd-eu-west-1.<your-team>.example.org "test zalando-cheat-sheet-generator application"

    $ ssh -L 63333:<ip-address>:8000 odd-eu-west-1.<your-team>.example.org

Now you can test via curl or browser:

.. code-block:: bash

    $ curl -v http://localhost:63333/index.html?schema=schema/stups.json

Route 100% traffic to your new stack version 1.

.. code-block:: bash

    $ senza traffic zalando-cheat-sheet-generator 1 100

Shut down the stack.

.. code-block:: bash

    $ senza delete zalando-cheat-sheet-generator 1
