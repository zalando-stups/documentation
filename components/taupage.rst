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

Using the Taupage AMI
++++++++++++++++++++++

There is currently no internal tooling but you can find the Taupage AMIs in your EC2 UI. They are maintained by the
STUPS team and regularly updated with the most recent security fixes and configuration improvements.

.. NOTE::
   The process of updating the AMI is not established nor discussed yet!

How to configure the AMI (configuration example)
++++++++++++++++++++++++++++++++++++++++++++++++

The Taupage AMI uses the official cloud-init project to receive user configuration. Different to the standard, you can
not use the normal user data mimetypes (no #cloud-config, shell scripts, file uploads, URL lists, ...) but only our own
configuration format::

   #taupage-ami-config

   application_id: my-nginx-test-app
   application_version: "1.0"

   runtime: Docker
   source: "pierone.example.org/myteam/nginx:1.0"

   ports:
     80: 80
     443: 443
     8301: 8301
     8301/udp: 8301
     8600: 8600/upd

   health_check_port: 80
   health_check_path: /

   environment:
     STAGE: production
     # environment variable values starting with "aws:kms:"
     # automatically are decrypted by Taupage
     MY_DB_PASSWORD: "aws:kms:v5V2bMGRgg2yTHXm5Fn..."

   capabilities_add:
     - NET_BIND_SERVICE
   capabilities_drop:
     - NET_ADMIN

   root: false
   privileged: false

   volumes:
     ebs:
       # attach EBS volume with "Name" tag "foo"
       /dev/sdf: foo
       # attach EBS volume with "Name" tag "bar"
       /dev/sdg: bar

     raid:
       # Defines RAID0 volume with the attached devices above (note the different device names)
       /dev/md/sampleraid0:
         level: 0
         devices:
           - /dev/xvdf
           - /dev/xvdg

   mounts:
     # Define a mountpoint for the above RAID volume which should be re-used without reformatting
     /some_volume:
       partition: /dev/md/sampleraid0
       erase_on_boot: false
       filesystem: ext4 # Default filesystem is ext4

     # An example for a non RAID configuration, which mounts regular devices on your EC2 instance
     /data:
       partition: /dev/xvdb
       erase_on_boot: true
     /data1:
       partition: /dev/xvdc
       filesystem: ext3

   notify_cfn:
     stack: pharos
     resource: WebServerGroup

   ssh_ports:
     - 22

   logentries_account_key: 12345-ACCOUNT-12345-KEY

   scalyr_account_key: 12345-ACCOUNTKEY-12234
   scalyr_application_log_parser: customParser

   mint_bucket: my-s3-mint-bucket

Provide this configuration as your user-data during launch of your EC2 instance.
You can use the ``TaupageConfig`` section of :ref:`senza`'s ``TaupageAutoScalingGroup``
to easily pass Taupage options when deploying with Senza.

Configuration option explanation
++++++++++++++++++++++++++++++++

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

The source, the configured runtime uses to fetch your deployment artifact. For Docker, this is the Docker image.
Usually this will point to a Docker image stored in :ref:`pierone`.

ports:
------

**(optional, default: no ports open)**

A map of all ports that have to be opened from the container. The key is the public server port to open and its value is the original port in your container. By default only TCP ports are opened. If you want to open UDP ports, you have to specify UDP protocol as a part of value or key::

   ports:
     8301: 8301  # open 8301 tcp port
     8301/udp: 8301  # open 8301 udp port
     8600: 8600/upd  # open 8600 udp port


environment:
------------

**(optional)**

A map of environment variables to set. Environment variable values starting with "aws:kms:" are automatically decrypted by Taupage using KMS (IAM role needs to allow decryption with the used KMS key).


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

hostname:
-----------------

**(optional)**

TBD, Users can define hostname by themselves

networking:
------------------

**(optional)**

A type of networking to tell how docker networks a container. See
https://docs.docker.com/articles/networking/#how-docker-networks-a-container for details.

Options are:
  * bridge (default)
  * host (This option also passes the hostname/instance name to the Docker container)
  * container:NAME_or_ID
  * none

root:
-----

**(optional, default: false)**

Specifies, if the container has to run as root. By default, containers run as an unprivileged user. See the
**capabilities_add** and prefer it always. This is only the last resort.

privileged:
-----------

**(optional, default: false)**

The container will run with --privileged option.
See https://docs.docker.com/reference/run/#runtime-privilege-linux-capabilities-and-lxc-configuration for more detail.

volumes:
--------

**(optional)**

Allows you to configure volumes that can later be mounted. Volumes accepts two sub-configurations - **EBS** and **RAID**.

EBS
^^^

The EBS sub-configuration expects key-value pairs of device name to EBS volumes. The "Name" tag is used to find the volumes.

Sample EBS volume configuration::

     ebs:
       /dev/sdf: solr-repeater-volume
       /dev/sdg: backup-volume

RAID
^^^^

The RAID sub-configuration allows you to describe RAID volumes by specifying the device name, usually */dev/md/your-raid-name*, and
all of the required RAID definitions.

You need to provide the RAID **level** and a collection of, at least, 2 **devices** to build your
RAID volume. The amount of devices is dependent on the RAID level. See http://en.wikipedia.org/wiki/Standard_RAID_levels#Comparison

Sample RAID volume configuration::

     raid:
       /dev/md/solr-repeater:
         level: 5
         devices:
           - /dev/xvdf
           - /dev/xvdg
           - /dev/xvdh

.. NOTE::
   EBS volumes are always attached first. This way you can use them in your RAID definitions.

   Depending on your instance virtualisation type, the final device names can be slightly different. Please refer to:

       * `AWS EC2 Block Device Mapping <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html>`_
       * `AWS EC2 Device Naming on Linux Instances <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html>`_

mounts:
-------

**(optional)**

A map of mount targets and their configurations. A mount target configuration has a **partition** to reference the volume, which can be
defined in the **volumes** section. It is possible to specify a **erase_on_boot** flag which determines is such partition should always
be initialized on boot. This setting defaults to false.

Whenever a partition is initialized is will be formatted using the **filesystem** setting. If unspecified it will be formatted as ext4. If **options** setting is specified, its value will be provided to the command to mount the partition. If the **root** setting is false (that's the default) the filesystem will be initialized with the internal unprivileged user as its owner. The mount point permissions are set to provide read and write access to group and others in all cases. This allows the **runtime** application to use the volume for read and write.

Sample mounts configuration::

   mounts:
     /data/solr:
       partition: /dev/md/solr-repeater
       options: noatime,nodiratime,nobarrier
       erase_on_boot: false

.. WARNING::
   Volumes without any partitions are initialized, even if **erase_on_boot** is set to False.

   Currently this check is done using extended filesystem tools and it was only tested against partitions using ext2, ext3 or ext4.

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

If you specify the Account Key from your logentries account, the Logentries Agent will be registered with your Account.
And the Agent will follow these logs:

  * /var/log/syslog
  * /var/log/auth.log
  * /var/log/audit.log
  * /var/log/application.log

You can get your Account Key from the Logentries Webinterface under /Account/Profile


scalyr_account_key
------------------

**(optional)**

If you provide the Scalyr AccountKey in the .yaml file, the agent of Scaylr will be installed and will follow these logs:

  * /var/log/syslog
  * /var/log/auth.log
  * /var/log/audit.log
  * /var/log/application.log

Our integration also provides some attributes you can search on Scalyr:

  * **$application_id**
  * **$application_version**
  * **$stack**
  * **$source**
  * **$image**

scalyr_application_log_parser
-----------------------------

**(optional)**

If the application.log format differs heavily between multiple applications the parser definition used by Scalyr can be overwritten here. The default value is `slf4j`.

Runtime environment
+++++++++++++++++++

By default, your application will run as an unprivileged user, see the 'root' option.

Taupage integrates :ref:`berry` and exposes the credentials file to your application. Your application will have access
to the environment variable 'CREDENTIALS_DIR', which points to a local directory, containing the 'user.json' and 'client.json' of
the :ref:`mint` API. This way, you can authenticate yourself to your own IAM solution so that it can obtain its own access
tokens.

Sending application mails
+++++++++++++++++++++++++

Mails which should be sent from applications can be sent out directly via Amazon SES.
The only thing you need to do is create an IAM user and receive SMTP credentials. This can be done directly in the SES menu.
Amazon already provides an example for Java: http://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-smtp-java.html

In order to use SES for sending out mails into the world, you need to request a limit increase (100 = 50k mails/day) to get
your account out of the sandbox mode.

AMI internals
+++++++++++++

This section gives you an overview of customization, the Taupage AMI contains on top of the Ubuntu Cloud Images.

Hardening
---------

TODO

* Kernel grsecurity, PAX?
* Restrictive file permissions (no unused SUID bins etc)
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

Building your own AMI
+++++++++++++++++++++

You can build your own Taupage AMI using the code from the repository on GitHub https://github.com/zalando-stups/taupage
In the repository you will find a configuration (config-stups-example.sh) file which you'll have to adjust to your needs.

See :ref:`taupage-ami-creation` for details.
