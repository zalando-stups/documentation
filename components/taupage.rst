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

   #taupage-ami-config

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
     # attach EBS with "Name" tag "FooBar"
     FooBar: /dev/sdh

   mounts:
     /var/lib/zookeeper-logs:
       devices:
         - /dev/sdb
       erase_on_boot: true
       filesystem: ext3 # default fs is ext4

     /var/lib/zookeeper-data:
       devices:
         - /dev/sdc
         - /dev/sdd
       raid_mode: 0 # Software RAID is not supported yet.
       erase_on_boot: true

   notify_cfn:
     stack: pharos
     resource: WebServerGroup

   ssh_ports:
     - 22

   logentries_account_key: 12345-ACCOUNT-12345-KEY
   logentries_token_id: 123456-TOKENID-123456

   scalyr_account_key: 12345-ACCOUNTKEY-12234

   mint_bucket: my-s3-mint-bucket

Provide this configuration as your user-data during launch of your EC2 instance.
You can use the ``TaupageConfig`` section of :ref:`senza`'s ``TaupageAutoScalingGroup``
to easily pass Taupage options when deploying with Senza.

application_id:
---------------

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

mounts:
-------

**(optional)**

A map of mount targets and device configurations. A device configuration has **device** to reference the root device
node and a **erase_on_boot** flag if the device should be partitioned and formatted on every boot (of not, the AMI expects and mounts
partition 1 from the device but partitions a new empty device).

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

logentries_account_key:
-----------------------

**(optional)**

If you specify the Account Key from you logentries account, the Logentries Agent will be registered with your Account.
And the Agent will follow these logs:

  * /var/log/syslog
  * /var/log/auth.log

You can get your Account Key from the Logentries Webinterface under /Account/Profile


logentries_token_id
-------------------

**(optional)**

You have to create a new "Manual Log" in the Webinterface.

For Example:

  * Create a new "Manual Log"
  * LogSet = APPLICATIONNAME
  * Log Name = APPLICATIONNAME-VERSION

Afterwards you get the **LogToken** and this token you have to set in the yaml file.

scalyr_account_key
------------------

**(optional)**

If you provide the Scalyr AccountKey in the .yaml file, the Agent of scaylr will be installed and follow this logs:

  * /var/log/syslog
  * /var/log/auth.log

Our integration also provide two Attributes you can search on Scalyr **$appname** and **$appversion**.

This attributes are filled with ``application_id`` (**$appname**) and ``application_version`` (**$appversion**)

Runtime environment
+++++++++++++++++++

By default, your application will run as an unprivileged user, see the 'root' option.

Taupage integrates :ref:`berry` and exposes the credentials file to your application. Your application will have access
to the environment variable 'CREDENTIALS_FILE', which points to a local file, containing the 'credentials.json' JSON of
the :ref:`mint` API. This way, you can authenticate yourself to your IAM solution to for example obtain own access
tokens.

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

Docker application logging
--------------------------

Application logs by Docker containers are streamed to syslog via Docker's logging driver for syslog as described
in the Docker documentation: https://docs.docker.com/reference/run/#logging-driver-syslog

Managed SSH access
------------------

SSH access is managed with the :ref:`even` SSH access granting service. The AMI is set up to have automatic integration. Your
SSH key pair choice on AWS will be ignored - temporary access can only be gained via the granting service. All user
actions are logged for auditing reasons. See the :ref:`ssh-access` section in the User's Guide for details.
