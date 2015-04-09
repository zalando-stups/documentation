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

Listing Stacks

.. code-block:: bash

    $ senza list myapp.yaml       # list only active stacks for myapp
    $ senza list myapp.yaml --all # list stacks for myapp (also deleted ones)
    $ senza list                  # list all active stacks
    $ senza list --all            # list all stacks (including deleted ones)

Deleting Stacks

.. code-block:: bash

    $ senza delete myapp.yaml 1

Senza Definition
================



Senza Components
----------------

Senza::StupsAutoConfiguration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **StupsAutoConfiguration** component autodetects load balancer and server subnets by relying on STUPS' naming convention (DMZ subnets have "dmz" in their name). It also finds the latest Taupage AMI and defines an image "LatestTaupageImage" which can be used by the "TaupageAutoScalingGroup" component.

Example usage:

.. code-block:: yaml

    SenzaComponents:
      - Configuration:
          Type: Senza::StupsAutoConfiguration

Senza::TaupageAutoScalingGroup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **TaupageAutoScalingGroup** component creates one AWS AutoScalingGroup resource with a LaunchConfiguration for the Taupage AMI.

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


Senza::WeightedDnsElasticLoadBalancer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **WeightedDnsElasticLoadBalancer** component creates one HTTPs ELB resource with Route 53 weighted domains.
The SSL certificate name used by the ELB can either be given (``SSLCertificateId``) or is autodetected.
The default Route53 hosted zone is used for the domain name.

.. code-block:: yaml

    SenzaComponents:
      - AppLoadBalancer:
          Type: Senza::WeightedDnsElasticLoadBalancer
          HTTPPort: 8080
          SecurityGroups:
            - app-myapp-lb

