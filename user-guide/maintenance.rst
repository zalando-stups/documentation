===========
Maintenance
===========

This section will cover the most frequent maintenance tasks you will face when running applications on the STUPS infrastructure.

Finding the latest Taupage AMI
==============================

You should regularly (at least every month) check your running stacks for :ref:`Taupage` updates.
:ref:`Senza` provides the convenience ``images`` command to see all used and most recent Taupage AMIs in your AWS account.

.. code-block:: bash

    $ senza images

Check the last column and identify all stacks still running with old AMIs.
The next section explains how to update them.

Updating Taupage AMI
====================

Senza allows updating launch configurations of running Cloud Formation stacks to use the latest Taupage AMI.

.. code-block:: bash

    $ senza patch mystack 1 --image=latest

The ``patch`` command will not affect any running EC2 instances, but all new instances launched in the respective Auto Scaling Group of mystack will now use the latest Taupage AMI.

The Senza ``respawn-instances`` command allows performing a rolling update of all EC2 instances in the Auto Scaling Group.

.. caution::

    The ``respawn-instances`` command will **terminate** running instances and thus should only be run on **stateless application stacks**.

.. code-block:: bash

    $ senza respawn-instances mystack 1

The process of respawn-instances is as follows:

* Suspend all ASG scaling activities
* Increase the ASG capacity by one (n+1).
* Wait for all n+1 instances to become healthy in associated ELB (if any)
* Terminate one old instance.
* Repeat until all n instances use the desired launch configuration.
* Reset the ASG capacity to the initial value (n)
* Resume all Scaling activities

This process allows updating to the latest Taupage AMI without any downtime as long as:

* The application is **stateless**, i.e. EC2 instances can be terminated without losing data.
* The ELB has connection draining enabled, i.e. instance termination waits for all in-flight requests to complete

Updating Docker Image
=====================

You can update the launch configuration's user data (Taupage YAML) to use a different Docker image:

.. code-block:: bash

    $ senza patch mystack 1 --user-data 'source: pierone.example.org/myteam/myart:1.2'

Afterwards you can use the ``respawn-instances`` command to apply the change to all instances.

Please note that we generally recommend to use the Immutable Stack approach for stateless applications. We consider patching the Docker Image in  launch configurations only for "emergency" hot deploys where every minute counts. Deploying immutable stacks via fully automated Continuous Delivery pipelines is considered best practice.

Redeploying odd
================

The :ref:`odd` SSH bastion host is running a standard Taupage image and should be updated regularly. The odd setup differs from usual application deployments as it runs in a public DMZ subnet and uses a public Elastic IP
To redeploy the odd SSH bastion host, you have to:

* start a new odd instance with the same launch configuration into one of the DMZ subnets.
* wait for it to be reachable (SSH port 22)
* detach the Elastic IP from the old odd
* attach the Elastic IP to the new odd instance
* shut down the old odd instance


