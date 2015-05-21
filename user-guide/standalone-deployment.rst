.. _standalone-deployment:

=====================
Standalone Deployment
=====================

.. Note::

   This section is only for users **without** an existing STUPS infrastructure!

Usually the STUPS deployment tooling relies on a completely configured STUPS environment, including:

* a specific STUPS AWS account VPC setup
* a private :ref:`pierone` registry (OAuth secured)
* and a private :ref:`taupage` AMI with baked in configuration

However, you can try out :ref:`senza` deployments with a publicly available :ref:`taupage` AMI.

This page will explain how to try out Senza with a default AWS VPC setup and the public Taupage AMI.


Prerequisites
=============

You need an fresh AWS account with:

* a default AWS VPC setup
  * VPC CIDR: 172.31.0.0/16
  * all subnets are public and have an internet gateway
* a hosted zone in Route 53 (e.g. "\*.stups.example.org") (you don't need to have nameserver delegation for testing)
* a SSL server certificate for your domain (e.g. "\*.stups.example.org") uploaded to IAM and named after your domain (dots replaced with hyphens, i.e. "stups-example-org"). A self-signed certificate will also do for testing.

Installing Senza
================

First install Python 3.4 on your PC (Ubuntu 14.04 already has it installed, use Homebrew on Mac).

.. Note::

    OS X users may need to set their locale environment to UTF-8 with::

        export LC_ALL=en_US.utf-8
        export LANG=en_US.utf-8

Senza can be installed from PyPI using PIP:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-senza

Check that the installation went fine by printing Senza's version number:

.. code-block:: bash

    $ senza --version

Configuring AWS Credentials
===========================

Senza needs access to your AWS account, so make sure you have your IAM user's access key in ``~/.aws/credentials``:

.. code-block:: bash

    $ cat ~/.aws/credentials
    [default]
    aws_access_key_id = ASIAJK123456789
    aws_secret_access_key = Ygx123i56789abc

Senza uses the AWS CLI's configuration file to know the AWS region you want to deploy to, so make sure you have it set correctly:

.. code-block:: bash

    $ cat ~/.aws/config
    [default]
    region = us-east-1

We will assume you have the AWS credentials and region (we use "us-east-1" in this example) correctly set for the remainder of this section.

Let's try out that Senza can call our AWS API:

.. code-block:: bash

    $ senza li
    Stack Name│Ver.│Status│Created│Description

The ``senza list`` command should print an empty table (just column headers) as we haven't deployed any Cloud Formation stack yet.


Bootstrapping a new Senza Definition
====================================

A Senza definition is essentially a Cloud Formation template as YAML with support for custom Senza components.

We need to create a new Senza definition YAML file to deploy our "Hello World" application:

.. code-block:: bash

    $ senza init helloworld.yaml
    Please select the project template
    1) bgapp: Background app with single EC2 instance
    2) postgresapp: HA Postgres app, which needs an S3 bucket to store WAL files
    3) webapp: HTTP app with auto scaling, ELB and DNS
    Please select (1-3): 3
    Application ID [hello-world]:
    Docker image without tag/version (e.g. "pierone.example.org/myteam/myapp") [stups/hello-world]:
    HTTP port [8080]:
    HTTP health check path [/]:
    EC2 instance type [t2.micro]:
    Mint S3 bucket name [example-stups-mint-123456789123-us-east-1]:
    Checking security group app-hello-world.. OK
    Security group app-hello-world does not exist. Do you want Senza to create it now? [Y/n]:
    Checking security group app-hello-world-lb.. OK
    Security group app-hello-world-lb does not exist. Do you want Senza to create it now? [Y/n]:
    Checking IAM role app-hello-world.. OK
    Creating IAM role app-hello-world.. OK
    Updating IAM role policy of app-hello-world.. OK
    Generating Senza definition file helloworld.yaml.. OK


Senza init will ask you a bunch of question, for our "Hello World" example, you only have to choose the "webapp" template and confirm the default answers with "RETURN".

The selected "webapp" template already takes care of creating the necessary security groups ("app-hello-world*") and IAM role ("app-hello-world").

We can check the generated Cloud Formation JSON by running ``senza print`` on our newly generated Senza definition:

.. code-block:: bash

    $ senza print helloworld.yaml v1 0.1 # first parameter is stack version, second is Docker image tag
    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Hello World (ImageVersion: 0.1)",
        "Mappings": {
            "Images": {
            ...
    # long Cloud Formation JSON after here...



Deploying a new Senza Application Stack
=======================================

Let's deploy a new immutable application stack using our Senza definition:

.. code-block:: bash

    $ senza create helloworld.yaml v1 0.1 # first parameter is stack version, second is Docker image tag
    Generating Cloud Formation template.. OK
    Creating Cloud Formation stack hello-world-v1.. OK

Our Senza ``list`` command output should now look different:

.. code-block:: bash

    $ senza li
    Stack Name │Ver.│Status            │Created│Description
    hello-world v1   CREATE_IN_PROGRESS 16s ago Hello World (ImageVersion: 0.1)




