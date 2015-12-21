==========
Monitoring
==========

This section should describe how to monitor applications running on the STUPS infrastructure.

CloudWatch Metrics
==================

The most basic monitoring can be achieved by the out-of-the-box `AWS CloudWatch`_ metrics.
CloudWatch monitoring is automatically enabled for EC2 instances deployed with :ref:`senza`.

CloudWatch EC2 metrics contain the following information:

* CPU Utilization
* Network traffic
* Disk throughput / operations per second - only for ephemeral storage, EBS volumes are not included

Taupage Monitoring Features
===========================

The :ref:`taupage` AMI supports a few features for enhanced monitoring:

* Enhanced CloudWatch metrics to monitor memory and diskspace: enable with ``enhanced_cloudwatch_metrics`` property in Taupage config (this allows monitoring RAM usage and root filesystem on EBS)
* `Prometheus Node Exporter`_ to export system metrics: the Prometheus Node Exporter is automatically started on every Taupage EC2 instance on port 9100

ZMON
====

The `ZMON Zalando monitoring tool`_ can be deployed into each AWS account to allow cross-team monitoring and dashboards. Make sure that ZMON appliance is allowed by security groups to connect to port 9100 of monitored instances.

ZMON allows querying arbitrary CloudWatch metrics using the `"cloudwatch()" check command`_.

ZMON allows parsing the Prometheus metrics using the the `"http().prometheus()" check command`_.



.. _AWS CloudWatch: http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/WhatIsCloudWatch.html
.. _Prometheus Node Exporter: https://github.com/prometheus/node_exporter
.. _ZMON Zalando monitoring tool: https://github.com/zalando/zmon
.. _"cloudwatch()" check command: http://zmon.readthedocs.org/en/latest/user/check-commands.html#cloudwatch
.. _"http().prometheus()" check command: http://zmon.readthedocs.org/en/latest/user/check-commands.html#prometheus
