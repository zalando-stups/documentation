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
