.. _taupage:

=======
Taupage
=======

**Taupage** is the base AMI allowing dockerized applications to run with STUPS.

As we want to foster immutable (and therefore deterministic and reproducible) deployments, we want to encourage the use
of Docker (and similar deployment technologies). The Taupage AMI is capable of starting a Docker container on boot. This
will enable teams to deploy 'what they want' as long as they package it in a Docker image. The server will be
set up to have an optimal configuration including managed SSH access, audit logging, log collection, monitoring and
reviewed security additions.

---------------------
Using the Taupage AMI
---------------------

There is currently no internal tooling but you can find the Taupage AMIs in your EC2 UI. They are maintained by the
Platform team and regularly updated with the newest security fixes and configuration improvements.

.. NOTE::
   The process of updating the AMI is not established nor discussed yet!

How to configure the AMI
++++++++++++++++++++++++

The Taupage AMI uses the official cloud-init project to receive user configuration. Different to the standard, you can
not use the normal user data mimetypes (no #cloud-config, shell scripts, file uploads, URL lists, ...) but only our own
configuration format::

   #zalando-ami-config

   application_id: my-nginx-test-app
   application_version: "1.0"

   runtime: Docker
   source: dockerfiles/nginx:latest

   ports:
     80: 80
     443: 443

   environment:
     STAGE: production

   capabilities_add:
     - NET_BIND_SERVICE
   capabilities_drop:
     - NET_ADMIN

   root: false

   volumes:
     ebs:
       /dev/sdf: taupage-ami-test-vol1
       /dev/sdg: taupage-ami-test-vol2
       /dev/sdh: taupage-ami-test-vol3
       /dev/sdi: taupage-ami-test-vol4

     raid:
       /dev/md/sampleraid0:
         level: 0
         devices:
           - /dev/xvdf
           - /dev/xvdg
       /dev/md/sampleraid1:
         level: 1
         devices:
           - /dev/xvdh
           - /dev/xvdi

   mounts:
     /some_volume:
       partition: /dev/md/sampleraid0
       erase_on_boot: false
       filesystem: ext4
     /other_volume:
       partition: /dev/md/sampleraid1


   notify_cfn:
     stack: pharos
     resource: WebServerGroup

   ssh_ports:
     - 22

Provide this configuration as your user-data during launch of your EC2 instance.
You can use the ``TaupageConfig`` section of :ref:`senza`'s ``TaupageAutoScalingGroup``
to easily pass Taupage options when deploying with Senza.

application_id:
-----------------

**(required)**

The well-known, registered (in :ref:`kio`) application identifier/name. Examples: "order-engine", "eventlog-service", ..

application_version:
--------------------

**(required)**

The well-known, registered (in :ref:`kio`) application version string. Examples: "1.0", "0.1-alpha", ..

runtime:
--------

**(required)**

What kind of deployment artifact you are using. Currently supported:

* Docker

.. NOTE::
   We plan to integrate CoreOS's Rocket as a runtime for experimental use soon.

source:
-------

**(required)**

The source, the configured runtime uses to fetch your delpoyment artifact. For Docker, this is the Docker image.
Usually this will point to a Docker image stored in :ref:`pierone`.

ports:
------

**(optional, default: no ports open)**

A map of all ports that have to be opened from the container. The key is the original port in your container and its
value is the public server port to open.

environment:
------------

**(optional)**

A map of environment variables to set.

capabilities_add:
-----------------

**(optional)**

A list of capabilities to add to the execution (without the CAP_ prefix). See
http://man7.org/linux/man-pages/man7/capabilities.7.html for available capabilities.

capabilities_drop:
------------------

**(optional)**

A list of capabilities to drop of the execution (without the CAP_ prefix). See
http://man7.org/linux/man-pages/man7/capabilities.7.html for available capabilities.

root:
-----

**(optional, default: false)**

Specifies, if the container has to run as root. By default, containers run as an unprivileged user. See the
**capabilities_add** and prefer it always. This is only the last resort.

volumes:
--------

**(optional)**

Allows you to configure volumes that can later be mounted. Volumes accepts two sub-configurations - **ebs** and **raid**.

The EBS sub-configuration expects key-value pairs of device name to EBS volumes (the Name tag is used to match the volume names).
Sample EBS volume configuration::

     ebs:
       /dev/sdf: solr-repeater-volume

The RAID sub-configuration allows you to describe RAID volumes by specifying the device name, usually /dev/md/your-raid-name and
all of the required RAID definitions. You need to provide the RAID **level** and a collection of, at least, 2 devices to build your
RAID volume. The amount of devices is dependant on the RAID level. See http://en.wikipedia.org/wiki/Standard_RAID_levels#Comparison
Sample RAID volume configuration::

     raid:
       /dev/md/solr-repeater:
         level: 5
         devices:
           - /dev/xvdf
           - /dev/xvdg
           - /dev/xvdh

.. NOTE::
   EBS volumes are always attached first. This way you can use them in your RAID definitions. Depending on your instance
   virtualization type, the final device names can be slightly different. Please refer to:
       http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
       http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html

mounts:
-------

**(optional)**

A map of mount targets and their configurations. A mount target configuration has a **partition** to reference the volume, which can be
defined in the **volumes** section. It is possible to specify a **erase_on_boot** flag which determines is such partition should always
be initialized on boot. This setting defaults to false. Whenever a partition is initialized is will be formatted using the **filesystem**
setting. If unspecified it will be formatted as ext4. If the **root** setting is false (that's the default) the filesystem will be
initialized with the internal unpriviledged user as its owner. This allows the **runtime** application to use the volume for read and write.

Sample mounts configuration::

   mounts:
     /data/solr:
       partition: /dev/md/solr-repeater
       erase_on_boot: false

.. WARNING::
   Volumes without any partitions are initialized, even if **erase_on_boot** is set to False. Currently this check is done using extended
   filesystem tools and it was only tested against partitions using ext2, ext3 or ext4.

notify_cfn:
-----------

**(optional)**

Will send cloud formation the boot result if specified. If you specify it, you have to provide the **stack** name and
the stack **resource** with which this server was booted. This helps cloud formation to know, if starting you server
worked or not (else, it will run into a timeout, waiting for notifications to arrive).

If you would use the example stack
http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/example-templates-autoscaling.html
the resource name would be **WebServerGroup**.

ssh_ports:
----------

**(optional, default: 22)**

List of SSH server ports. This option allows using alternative TCP ports for the OpenSSH server.
This is useful if an application (runtime container) wants to use the default SSH port.

AMI internals
+++++++++++++

This section gives you an overview of customization, the Taupage AMI contains on top of the Ubuntu Cloud Images.

Hardening
---------

TODO

* Kernel grsecurity, PAX?
* Resrictive file permissions (no unused SUID bins etc)
* Unused users and groups removed
* Unused daemons disabled
* Zalando CA preinstalled
* Weak crypto algorithms disabled (SSH)
* Unused packages removed
* No passwords for users
* iptables preconfigured with only specified ports + ssh open
* hardened network settings (sysctl)
* disabled IPv6 (not possible in AWS anyways)

Auditing & Logs
---------------

TODO

* auditd logs all access
* all logs, including application logs (docker logs) are streamed to central logging service and rotated

Managed SSH access
------------------

SSH access is managed with the :ref:`even` SSH access granting service. The AMI is set up to have automatic integration. Your
SSH key pair choice on AWS will be ignored - temporary access can only be gained via the granting service. All user
actions are logged for auditing reasons. See the :ref:`ssh-access` section in the User's Guide for details.
