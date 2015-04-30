.. _senza:

=====
Senza
=====

**Senza** is STUPS' deployment tool to create and execute `AWS CloudFormation templates`_ in a sane way.

See the :ref:`deployment` section for details on how to deploy applications using Senza, :ref:`pierone` and :ref:`taupage`.

Installation
============

Install or upgrade to the latest version of Senza (|senza-pypi-version|) with PIP:

.. |senza-pypi-version| image:: https://img.shields.io/pypi/v/stups-senza.svg
   :target: https://pypi.python.org/pypi/stups-senza/
   :alt: Latest PyPI version

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-senza


Command Line Usage
==================

Senza definitions can be bootstrapped conveniently to get started quickly:

.. code-block:: bash

    $ senza init myapp.yaml

Cloud Formation stacks are created from Senza definitions with the ``create`` command:

.. code-block:: bash

    $ senza create myapp.yaml 1 0.1-SNAPSHOT

You can disable the automatic Cloud Formation rollback-on-failure in order to do 'post-mortem' debugging (e.g. on an EC2 instance):

.. code-block:: bash

    $ senza create --disable-rollback myerroneous-stack.yaml 1

Stacks can be listed using the ``list`` command:

.. code-block:: bash

    $ senza list myapp.yaml       # list only active stacks for myapp
    $ senza list myapp.yaml --all # list stacks for myapp (also deleted ones)
    $ senza list                  # list all active stacks
    $ senza list --all            # list all stacks (including deleted ones)

There are a few commands to get more detailed information about stacks:

.. code-block:: bash

    $ senza resources myapp.yaml 1 # list all CF resources
    $ senza events myapp.yaml 1    # list all CF events
    $ senza instances myapp.yaml 1 # list EC2 instances and IPs

Traffic can be routed via Route53 DNS to your new stack:

.. code-block:: bash

    $ senza traffic myapp.yaml      # show traffic distribution
    $ senza traffic myapp.yaml 2 50 # give version 2 50% of traffic

Stacks can be deleted when they are no longer used:

.. code-block:: bash

    $ senza delete myapp.yaml 1

.. Tip::

    All commands and subcommands can be abbreviated, i.e. the following lines are equivalent:

    .. code-block:: bash

        $ senza list
        $ senza l

Bash Completion
---------------

The programmable completion feature in Bash permits typing a partial command, then pressing the :kbd:`[Tab]` key to auto-complete the command sequence.
If multiple completions are possible, then :kbd:`[Tab]` lists them all.

To activate bash completion for the Senza CLI, just run:

.. code-block:: bash

    $ eval "$(_SENZA_COMPLETE=source senza)"

Put the eval line into your :file:`.bashrc`:

.. code-block:: bash

    $ echo 'eval "$(_SENZA_COMPLETE=source senza)"' >> ~/.bashrc

.. _senza-definition:

Senza Definition
================

Senza definitions are Cloud Formation templates as YAML with added 'components' on top.
A minimal Senza definition without any Senza components would look like:

.. code-block:: yaml

    Description: "A minimal Cloud Formation stack creating a SQS queue"
    SenzaInfo:
      StackName: example
    Resources:
      MyQueue:
        Type: AWS::SQS::Queue

.. Tip::

    Use ``senza init`` to quickly bootstrap a new Senza definition YAML for most common use cases (e.g. a web application).

During evaluation of the definition, mustache templating is applied with access to the rendered definition,
including the SenzaInfo, SenzaComponents and Arguments key (containing all given arguments).

Senza Info
----------

The ``SenzaInfo`` key must always be present in the definition YAML and configures global Senza behavior.

Available properties for the ``SenzaInfo`` section are:

``StackName``
    The stack name (required).
``OperatorTopicId``
    Optional SNS topic name or ARN for Cloud Formation notifications. This can used for example to send notifications about deployments to a mailing list.
``Parameters``
    Custom Senza definition parameters. This can be used to dynamically substitute variables in the Cloud Formation template.


Senza Components
----------------

Components are predefined Cloud Formation snippets that are easy to configure and generate all the boilerplate JSON that is required by Cloud Formation.

All Senza components must be configured in a list below the top-level "SenzaComponents" key, the structure is as follows:

.. code-block:: yaml

    SenzaComponents:
      - ComponentName1:
          Type: ComponentType1
          SomeComponentProperty: "some value"
      - ComponentName2:
          Type: ComponentType2

.. Note::

    Please note that each list item below "SenzaComponents" is a map with only one key (the component name).
    The YAML "flow-style" syntax would be: ``SenzaComponents: [{CompName: {Type: CompType}}]``.


Senza::StupsAutoConfiguration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **StupsAutoConfiguration** component type autodetects load balancer and server subnets by relying on STUPS' naming convention (DMZ subnets have "dmz" in their name). It also finds the latest Taupage AMI and defines an image "LatestTaupageImage" which can be used by the "TaupageAutoScalingGroup" component.

Example usage:

.. code-block:: yaml

    SenzaComponents:
      - Configuration:
          Type: Senza::StupsAutoConfiguration

.. _senza-taupage-auto-scaling-group:

Senza::TaupageAutoScalingGroup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **TaupageAutoScalingGroup** component type creates one AWS AutoScalingGroup resource with a LaunchConfiguration for the Taupage AMI.

.. code-block:: yaml

    SenzaComponents:
      - AppServer:
          Type: Senza::TaupageAutoScalingGroup
          InstanceType: t2.micro
          SecurityGroups:
            - app-myapp
          ElasticLoadBalancer: AppLoadBalancer
          TaupageConfig:
            runtime: Docker
            source: foobar/myapp:1.0
            ports:
              8080: 8080
            environment:
              FOO: bar

This component supports the following configuration properties:

``InstanceType``
    The EC2 instance type to use.
``SecurityGroups``
    List of security groups to associate the EC2 instances with. Each list item can be either an existing security group name or ID.
``IamInstanceProfile``
    ARN of the IAM instance profile to use. You can either use "IamInstanceProfile" or "IamRoles", but not both.
``IamRoles``
    List of IAM role names to use for the automatically created instance profile.
``Image``
    AMI to use, defaults to ``LatestTaupageImage``.
``ElasticLoadBalancer``
    Name of the ELB resource.
``TaupageConfig``
    Taupage AMI config, see :ref:`taupage` for details.
    At least the properties ``runtime`` ("Docker") and ``source`` (Docker image) are required.
    Usually you will want to specify ``ports`` and ``environment`` too.
``AutoScaling``
    Map of auto scaling properties, see below.

``AutoScaling`` properties are:

``Minimum``
    Minimum number of instances to spawn.
``Maximum``
    Maximum number of instances to spawn.
``MetricType``
    Metric to do auto scaling on, only supported value is ``CPU``
``ScaleUpThreshold``
    On which value of the metric to scale up. For the "CPU" metric: a value of 70 would mean 70% CPU usage.
``ScaleDownThreshold``
    On which value of the metric to scale down. For the "CPU" metric: a value of 40 would mean 40% CPU usage.



Senza::WeightedDnsElasticLoadBalancer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **WeightedDnsElasticLoadBalancer** component type creates one HTTPs ELB resource with Route 53 weighted domains.
The SSL certificate name used by the ELB can either be given (``SSLCertificateId``) or is autodetected.
You can specify the main domain (``MainDomain``) or the default Route53 hosted zone is used for the domain name.

.. code-block:: yaml

    SenzaComponents:
      - AppLoadBalancer:
          Type: Senza::WeightedDnsElasticLoadBalancer
          HTTPPort: 8080
          SecurityGroups:
            - app-myapp-lb

The WeightedDnsElasticLoadBalancer component supports the following configuration properties:

``HTTPPort``
    The HTTP port used by the EC2 instances.
``HealthCheckPath``
    HTTP path to use for health check (must return 200), e.g. "/health"
``SecurityGroups``
    List of security groups to use for the ELB. The security groups must allow SSL traffic.
``MainDomain``
    Main domain to use, e.g. "myapp.example.org"
``VersionDomain``
    Version domain to use, e.g. "myapp-1.example.org"



.. _AWS CloudFormation templates: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html
