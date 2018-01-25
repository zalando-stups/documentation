.. _ssh-access:

==========
SSH Access
==========

Every team member can get access to any of the team's EC2 instances by using the :ref:`piu` command line tool:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-piu
    $ # assumptions: region is Ireland, team name is "myteam", private EC2 instance has IP "172.31.146.1"
    $ piu 172.31.146.1 "Troubleshoot problem XY"
    # enter even URL (e.g. https://even.stups.example.org)
    # enter odd hostname "odd-eu-west-1.myteam.example.org"
    $ ssh -A odd-eu-west-1.myteam.example.org # agent-forwarding must be used!
    $ ssh 172.31.146.1 # jump from bastion to private instance

.. Tip::

    Use the ``--connect`` flag to directly connect to the EC2 instance so you do not need to execute the SSH command yourself.

.. Tip::

    Use the **interactive mode** to experience an easy way to access instances. This mode prompts you for the AWS region where your instance is located, so it can present you a list of enumerated deployed stacks from which you can choose the one you want to access and provide a reason for it.

    To get the most of this mode, it's recommended that piu is invoked with the ``--connect`` flag so you get into the instance as soon as the odd host authorizes your request: ``$ piu request-access --interactive --connect``. Alternatively, you can set the ``PIU_CONNECT`` and ``PIU_INTERACTIVE`` environment variables in your shell profile so you can invoke the command with the mentioned features enabled just with: ``$ piu request-access``.

.. Tip::

    If executing a **piu** command results in a message ``Access to host odd-eu-west-1.myteam.example.org for user <myuser> was granted.``, but you get an error ``Permission denied (publickey).``, you can solve this by installing an **ssh-agent** and executing ``ssh-add`` prior to **piu**. 

.. Tip::

    Use the ``--clip`` option to copy the output of piu to your clipboard.
    On Linux it requires the package ``xclip``. On OSX it works out of the box.

.. Tip::

    Use ``senza instances`` to quickly get the IP address of your EC2 instance.
    See the :ref:`Senza reference <senza>` for details.

Più will remember the URL of :ref:`even` and the hostname of :ref:`odd` in the local config file (``~/.config/piu/piu.yaml`` on Linux).
You can overwrite settings on the command line:

.. code-block:: bash

    $ piu 172.31.1.1 test -O odd-eu-west-1.myotherteam.example.org


.. Caution::

    All user actions are logged for auditing reasons, therefore all **SSH sessions must be kept free of
    any sensitive and/or personal information**.

Check the asciicast how using :ref:`piu` looks like:

.. raw:: html

    <script type="text/javascript" src="https://asciinema.org/a/25671.js" id="asciicast-25671" async></script>

Copying Files
=============

As all access to an EC2 instance has to go through the :ref:`odd` SSH jump host,
copying files from and to the EC2 instance appears unnecessary hard at first.

Luckily OpenSSH's ``scp`` supports jump hosts with the ``ProxyCommand`` configuration option:

.. code-block:: bash

    $ scp -o ProxyCommand="ssh -W %h:%p odd-eu-west-1.myteam.example.org" mylocalfile.txt 172.31.146.1:

See also the `OpenSSH Cookbook on Proxies and Jump Hosts`_.


SSH Access Revocation
=====================

SSH access will automatically be revoked by :ref:`even` after the request's lifetime (default: 60 minutes) expired.
You can specify a non-default lifetime by using Più's ``-t`` option.

Listing Access Requests
=======================

The :ref:`even` SSH access granting service stores all access requests and their status in a database.
This information is exposed via REST and can be shown using Più's "list-access-requests" command.

All current and historic access requests can be listed on the command line:

.. code-block:: bash

    $ piu list                   # list the most recent requests to my odd host
    $ piu list -U jdoe -O '*'    # list most recent requests by user "jdoe"
    $ piu list -O '*' -s GRANTED # show all active access requests


.. _OpenSSH Cookbook on Proxies and Jump Hosts: https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Proxies_and_Jump_Hosts
