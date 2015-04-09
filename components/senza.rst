.. _senza:

=====
Senza
=====

**Senza** is STUPS' deployment tool.

See the :ref:`deployment` section for details on how to deploy applications using Senza, :ref:`pierone` and :ref:`taupage`.

Command Line Usage
==================

Creating Stacks

.. code-block:: bash

    $ senza create myapp.yaml 1 0.1-SNAPSHOT

You can disable the automatic Cloud Formation rollback-on-failure in order to do 'post-mortem' debugging (e.g. on an EC2 instance):

.. code-block:: bash

    $ senza create --disable-rollback myerroneous-stack.yaml 1

Listing Stacks

.. code-block:: bash

    $ senza list myapp.yaml       # list only active stacks for myapp
    $ senza list myapp.yaml --all # list stacks for myapp (also deleted ones)
    $ senza list                  # list all active stacks
    $ senza list --all            # list all stacks (including deleted ones)

Deleting Stacks

.. code-block:: bash

    $ senza delete myapp.yaml 1

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

Senza::TaupageAutoScalingGroup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **TaupageAutoScalingGroup** component type creates one AWS AutoScalingGroup resource with a LaunchConfiguration for the Taupage AMI.

.. code-block:: yaml

    SenzaComponents:
      - Configuration:
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
``ElasticLoadBalancer``
    Name of the ELB resource.
``TaupageConfig``
    Taupage AMI config, see :ref:`taupage` for details.


Senza::WeightedDnsElasticLoadBalancer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **WeightedDnsElasticLoadBalancer** component type creates one HTTPs ELB resource with Route 53 weighted domains.
The SSL certificate name used by the ELB can either be given (``SSLCertificateId``) or is autodetected.
The default Route53 hosted zone is used for the domain name.

.. code-block:: yaml

    SenzaComponents:
      - AppLoadBalancer:
          Type: Senza::WeightedDnsElasticLoadBalancer
          HTTPPort: 8080
          SecurityGroups:
            - app-myapp-lb

