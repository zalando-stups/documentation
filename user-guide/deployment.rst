.. _deployment:

==========
Deployment
==========

The :ref:`senza` command line tools allows deploying application stacks.
This page will guide you through the steps necessary to deploy
a Docker-based application with Senza.

Senza was primarily designed to deploy immutable stacks of web applications:

.. image:: images/application-stack.svg

Each immutable stack (application version) is a Cloud Formation stack
with a load balancer (ELB), an auto scaling group and a
versioned DNS domain.
Traffic can be routed to different application versions by changing DNS weights in Route53.

Deploying a new immutable application stack generally involves:

* building your application artifact (e.g. uber jar)
* creating a Docker image
* pushing the Docker image to the :ref:`pierone` Docker registry
* creating the Cloud Formation stack with Senza (``senza create``)
* routing traffic to the new stack (``senza traffic``)

.. image:: images/senza-deployment.png
   :alt: Deploying an application with Senza and Pier One

Prerequisites
=============

First install Python 3.4 on your PC (Ubuntu 14.04 already has it installed, use Homebrew on Mac).

.. Note::

    OS X users may need to set their locale environment to UTF-8 with::

        export LC_ALL=en_US.utf-8
        export LANG=en_US.utf-8

All required STUPS command line tools can be conveniently installed from PyPI using PIP:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups

You will need the following information at hand:

* Pier One Docker registry URL (we will use https://pierone.stups.example.org here)
* SAML identity provider URL (for federated AWS login with :ref:`Mai`)

  * your SAML username and password

* OAuth Token service URL (to acquire OAuth tokens, e.g. for Pier One)

  * your OAuth realm's username and password



Prepare the deployment artifact
===============================

First deploy the application's artifact (Docker image) to :ref:`pierone`, e.g.:

.. code-block:: bash

    $ cd myapp # enter your application's source folder
    $ # please remember to generate the "scm-source.json",
    $ # which must be in your Docker image!
    $ docker build -t pierone.stups.example.org/myteam/myapp:0.1 .
    $ pierone login # login to Pier One using OAuth
    $ docker push pierone.stups.example.org/myteam/myapp:0.1

Create a new Senza definition
=============================

In order to call AWS endpoints and to create the Cloud Formation stack, we need to login with :ref:`mai`:

.. code-block:: bash

    $ mai create myteam # create a new profile (if you haven't done so)
    $ mai # login

Next you need to create a new :ref:`Senza deployment definition YAML <senza-definition>` file.
This can be done conveniently with the ``senza init`` command:

.. code-block:: bash

    $ senza init myapp.yaml

.. Note::

    We assume you have your default AWS region ID (e.g. "eu-west-1") configured in ``~/.aws/config``, alternatively you can pass the ``--region`` option to Senza.
    See the `AWS CLI docs`_ for details.

``senza init`` will guide you through a bunch of questions.
Use the "webapp" template and choose the default answers to get a ready-to-use hello world application.
Senza will also create the necessary security groups for you.

Deploying your application with Senza
=====================================

Now we can create the application's Cloud Formation stack with Senza:

.. code-block:: bash

    $ senza create myapp.yaml 1 0.1

.. Note:: The last parameter is a custom parameter "ImageVersion" defined in the SenzaInfo/Parameters section of the above definition YAML.

The stack creation will take some time, we can use the ``events`` command to monitor the progress:

.. code-block:: bash

    $ senza events myapp.yaml 1 --watch=2

The ``--watch`` option tells Senza to refresh the display every 2 seconds until we press ``CTRL-C``.

The "events" command will eventually show ``CREATE_COMPLETE`` for the ``CloudFormation::Stack`` resource if everything went well.

Read the section :ref:`ssh-access` on how to get shell access to your EC2 instances (if needed).

Routing traffic to your application
===================================

Your new application stack should be accessible via the version domain, e.g. "myapp-1.example.org".
You can use the version domain to verify that your application is working (e.g. via automated regression tests).

Eventually you want to route "real" traffic via the main domain (e.g. "myapp.example.org") to your new application stack.
This can be done via Senza`s "traffic" command:

.. code-block:: bash

    $ senza traffic myapp.yaml 1 100 # route 100% traffic to stack version 1

Use ``dig`` to check whether the DNS settings are already updated:

.. code-block:: bash

    $ dig myapp-1.example.org
    > ;; ANSWER SECTION:
      myapp.exmaple.org. 20	IN	CNAME	myapp-1-123456789.eu-west-1.elb.amazonaws.com.
    $ # ^ this is good, myapp.example.org redirects to myapp-1.example.org

Depending on your physical location there might be a bunch of DNS caches between you and Amazon.
Since they do not update quickly you can enforce to check the AMZN DNS.
Look up the address of the nameservers in your AWS account (Route 53 -> example.org Hosted Zone Details -> Nameservers), they look like ``ns-123.awsdns-55.com``.

.. code-block:: bash

    $ dig myapp-1.example.org @ns-123.awsdns-55.com

.. _AWS CLI docs: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
