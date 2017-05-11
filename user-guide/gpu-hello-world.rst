=========================
A hello world GPU example
=========================

This guide should show you all the steps required for creating a simple GPU-based application. It is recommended that the reader familiarize themselves with :ref:`hello-world` and the other parts of the :ref:`user-guide` before getting started.

Clone the example project:

.. code-block:: bash

    $ git clone https://github.com/zalando-stups/gpu-hello-world.git
    $ cd gpu-hello-world

Create this new application using the :ref:`yourturn` web frontend:

.. code-block:: bash

    https://yourturn.stups.example.org

Now you will need to create the :ref:`scm-source-json` file that links your Docker image to a specific git revision number (here the `scm-source Python package <https://pypi.python.org/pypi/scm-source>`_ is used):

.. code-block:: bash

    $ scm-source

Build the Docker image

.. code-block:: bash

    $ docker build -t pierone.stups.example.org/<your-team>/gpu-hello-world:0.1 .

And now see if it is listed locally:

.. code-block:: bash

    $ docker images

If you have `nvidia-docker <https://github.com/NVIDIA/nvidia-docker>`_ installed locally, the image can also be run:

.. code-block:: bash

    $ docker run --rm -it pierone.stups.example.org/<your-team>/gpu-hello-world:0.1

which should show the expected output from `nvidia-smi`.

.. Note::

    Running with `docker` instead of `nvidia-docker` will show a `/bin/sh: 1: nvidia-smi: not found` message as the `nvidia-smi` tool used is part of the NVIDIA CUDA driver installiation which is not available when running with `docker`.

If all works, we are ready to login in :ref:`pierone` and push it.

.. code-block:: bash

    $ pierone login
    $ docker push pierone.stups.example.org/<your-team>/gpu-hello-world:0.1

Let's check if we can find it in the Pier One repository (login needed if your token expired):

.. code-block:: bash

    $ pierone login
    $ pierone tags <your-team> gpu-hello-world

Now let's create the version in YOUR TURN for the application created:

.. code-block:: bash

    https://yourturn.stups.example.org

Configure your application's mint bucket (click on the "Access Control" button on your app's page in YOUR TURN).

This will trigger the mint worker to write your app credentials to your mint bucket.

Deploy!

The repository contains an example :ref:`senza` definition that can be used to deploy the Hello World example. If required, you can also add a log provider or other configuration options (like :ref:`guide <spot-pricing>`).

The Cloud Formation stack can be created by running:

.. code-block:: bash

    $ senza create --region=eu-west-1 deploy-definition.yaml stackversion pierone.stups.example.org/<your-team>/gpu-hello-world 0.1 example-mint-bucket-eu-west-1

Note that this assumes a stack version of `stackversion` and a :ref:`pierone` image version of `0.1`.

Once the stack has started up, you should be able to view the output in your log provider (if configured). If not, the instance can be accessed and the contents of the `/var/log/application.log` checked to confirm that the stack ran as expected.
