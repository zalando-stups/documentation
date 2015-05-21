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

You need an AWS account and:

* a default AWS VPC setup
  * VPC CIDR: 172.31.0.0/16
  * all subnets are public and have an internet gateway
* a hosted zone in Route 53
