===============
Troubleshooting
===============

Permission issues when running Docker container on Taupage AMI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you get permission issues (e.g. ``chown: changing ownership of foobar: Operation not permitted``) when running your Docker image on Taupage,
you probably run a Docker image assuming to run as ``root``. Taupage starts Docker containers with an unprivileged user by default.
You can test your Docker image locally with ``docker run -u 998 ...``.
Usually all apps (especially JVM-based applications) should be able to run as non-root.
Sadly most Docker images from the official Docker Hub assume running as root.


If you really need to run your Docker container as ``root``, you can use the ``root: true`` Taupage config option.
See the :ref:`Taupage reference <taupage>` for details.


I cannot access my EC2 instance via SSH
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you can get access to :ref:`odd` via :ref:`piu`, but accessing your private EC2 instance does not work: First check your server's security group. It must allow inbound traffic on TCP port 22 (SSH) from the "odd" bastion host.

If you get a "Permission denied (publickey)" error, check that your local SSH key agent is running:

.. code-block:: bash

    $ ssh-add -l
    # this should list your private key(s) (e.g. id_rsa)
    
I get a 403 forbidden for piu? What could it be?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
403: Authentication failed -> is definitely your LDAP user/pass (check your keyring/keychain). Please ensure that your ssh public key is uploaded to zack and that your keyring (keychain in osx) contains the correct LDAP password for piu (delete it and try the piu command again). if you mistype it once at the beginning, piu always tries the wrong password.


If I changed my LDAP password recently, will this affect piu in some way?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

yes, it directly checks your password against LDAP. Please that your keyring (keychain in osx) contains the correct LDAP password for piu (delete it and try the piu command again). if you mistype it once at the beginning, piu always tries the wrong password.


If I use keyring in a shared linux maschine, everyone can get my LDAP password by keyring get piu xxx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just don't use a shared linux machine. And if you really have to use a shared linux machine -> linux is multi-user, just configure it accordingly (that no user can read other users files).


Is the agreement with amazon to store customer information already valid?

	yes, we signed a "DPA" (Data Protection Addendum) for the Enterprise Aggrement. This is valid for Ireland and Frankfurt

Via SSH acces I get the information Permission denied (publickey).
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If $ ssh-add -l says "could not open a connection to your authentication agent", then you must have a running key agend. The Solution you find here http://stups.readthedocs.org/en/latest/user-guide/troubleshooting.html


I get an Internal server error: 409 trying to push tag ...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

409 means Conflict which we send when you try to push an image or tag with an existing name again - pierone enforces immutability, you cannot push a tag twice.


What kind of SSL certificate I have to use in my Docker file?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://pierone.stups.zalan.do/ is now using a Comodo SSL cert, i.e. you should not need to put any CA cert config in Docker anymore


Can I use pierone from home office?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pierone is currently only available from the offices, aws and dcs. If you cnofigure your vpn connection to also route aws IPs via VPN then it should work .By default your VPN connection will not be used to access the public aws IPs, therefore you have a not-whitelisted IP


I get following error Message:  RRSet with DNS name "my.team" and type CNAME, SetIdentifier documentation-Version1 cannot be created as weighted sets must contain the same TTL.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You probably have a previous record in Route53 (e.g. created by AWS Minion), just set the Time To Live (TTL) to "20" for all records (Senza uses TTL of 20 by default)

How can i add the new relic licence key file to my docker image? or can i assume that it will be provided by the Taupage AMI? If the later, will it be still under /etc//etc/newrelic.licensekey ? only /etc/newrelic.licensekey obviously?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
E.g. for pharos we used the KMS service to encrypt the key. Here the repo: https://stash.zalando.net/projects/ASA/repos/strategy-architecture-management/browse/pharos-webapp. So the application is the only one how can read the key.
