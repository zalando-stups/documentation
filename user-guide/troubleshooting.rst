===============
Troubleshooting
===============

Senza stack creation fails with Cloud Formation ValidationError
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If Senza throws a Cloud Formation "ValidationError" at you when runnning ``senza create``, you can use ``senza print`` to debug the problem:

.. code-block:: bash

    $ senza create myapp.yaml 1 0.1
    {"Error":{"Code":"ValidationError","Message":"Template error: Mapping named 'LoadBalancerSubnets' is not present in the 'Mappings' section of template.","Type":"Sender"},"RequestId":"..."}

    $ senza print myapp.yaml 1 0.1 # first parameter is stack version, second is Docker image tag
    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Hello World (ImageVersion: 0.1)",
        "Mappings": {
            "Images": {
            ...
    # long Cloud Formation JSON after here...

You can always do ``senza print`` to look at the generated Cloud Formation JSON.
The ``print`` command does the same as the ``create`` command, but it just prints the CF JSON.

.. Tip::
    You can use the `jq`_ command-line JSON processor to pretty-print the generated JSON:

    .. code-block:: bash

        $ senza print helloworld.yaml v1 1.0 | jq .



Senza stack is rolled back automatically (status ROLLBACK_COMPLETE)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If your freshly created Senza stack keeps get rolled back by Cloud Formation after a few minutes, you can try debugging the problem by disabling the automatic rollback:

.. code-block:: bash

    $ senza create myapp.yaml 1 0.1
    # .. few minutes pass ..

    $ senza status myapp.yaml 1
    Stack Name │Ver.│Status           │Inst.#│Running│Healthy│LB Status│HTTP │Main DNS
    myapp       1    ROLLBACK_COMPLETE      0       0       0           ERROR no

    # first check the rollback reason
    $ senza events myapp.yaml 1 -o tsv
    # ...
    AutoScaling::AutoScalingGroup   AppServer   CREATE_FAILED   Failed to receive 1 resource signal(s) within the specified duration
    # ...

    $ senza create myapp.yaml 1 0.1 --disable-rollback
    # stack and EC2 instance(s) will stay up

.. Tip::
    Usually you can avoid SSH access and ``--disable--rollback`` by using a logging provider to see the :ref:`taupage` syslog messages.
    The Taupage AMI supports logentries_ and Scalyr_ as logging providers.


By disabling the automatic Cloud Formation rollback-on-failure, you can troubleshoot the problem on the EC2 instance via SSH.
See the :ref:`ssh-access` section on how to "ssh" into your EC2 instance (running Taupage AMI).

.. Note::
    The most common rollback reason is a failing EC2 instance not notifying Cloud Formation in time, e.g. because the application could not start (Docker download failed, etc).

    There are also less common failure reasons, e.g. when modifying the Senza stack definition by hand.
    Please check the "status_reason" column of ``senza events`` to see the Cloud Formation error message.




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


How to read Docker logs on EC2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Docker logs containing your application's STDOUT are written to Syslog.
After getting :ref:`ssh-access` to your EC2 instance (running the Taupage AMI), you can grep them:

.. code-block:: bash

    $ grep docker /var/log/syslog


No internet connection (connection timeouts) on EC2 instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you get connection timeouts on your EC2 instance, e.g. the Docker image download or SSH access fails (cannot download public SSH key from :ref:`even`):

* If your EC2 instance runs in a **DMZ subnet**: instances in DMZ subnets have no internet connection unless you assign a public IP.
  Usually you should start instances in internal subnets only and only use ELBs in the DMZ subnets.
* If your EC2 instance runs in an **Internal subnet**: check that your subnet routing table and NAT instance is working correctly.

Also check your instance's security group whether it allows outbound traffic.

.. _jq: https://stedolan.github.io/jq/
.. _logentries: https://logentries.com/
.. _Scalyr: https://www.scalyr.com/
