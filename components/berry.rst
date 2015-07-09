.. _berry:

=====
berry
=====

**berry** is the counterpart for :ref:`mint`. It is a small agent, that runs on a server and continuously checks for
password changes of an application's service user. Berry downloads the application's OAuth credentials from the given Mint S3 bucket into the specified credentials directory.
The application needs to periodically refresh its credentials from the credentials directory.

Berry can run on multiple environments:

* Berry automatically runs on :ref:`taupage` if the ``mint_bucket`` Taupage property is set
* Berry can run on non-AWS environments. In this case AWS credentials need to be provided.

Berry on Taupage
================

Berry starts automatically if the ``mint_bucket`` Taupage property is set. Berry will read its configuration (application ID) from ``/etc/taupage.yaml``.
The EC2 instance needs to be started with an instance profile (IAM role) with permissions to read from the Mint S3 bucket (``senza init`` takes care of that).
Credentials will be downloaded to ``/meta/credentials``. Berry logs to syslog using the ``berry`` tag.

Berry on Non-AWS
================

Berry supports some convenience options to run on non-AWS environments:

* You can specify an alternate configuration file to read (``-f`` option). This allows packaging a ``berry.yaml`` (defining ``application_id``, ``mint_bucket`` and ``region``) in the application's deployment artifact to start Berry from the application's start script.
* You can specify a special AWS credentials lookup file (``-c`` option). This allows rolling out per-application AWS credentials centrally in your environment through some "secure" distribution mechanism (e.g. GPG + agent).

An example command line to start Berry for an instance of "myapp" might look like:

.. code-block:: bash

    $ berry -f /webapps/myapp/berry.yaml -c /etc/aws-creds-by-app /webapps-data/myapp/meta/credentials

The ``/webapps/myapp/berry.yaml`` file might look like:

.. code-block:: yaml

    ---
    application_id: myapp
    mint_bucket: mint-example-bucket
    region: eu-central-1

The ``/etc/aws-creds-by-app`` file might look like:

.. code-block:: bash

    # this file contains AWS access keys for berry
    # each line has three columns separated by colon (":"):
    # <application_id>:<access_key_id>:<secret_access_key>
    myapp:ABC123:xyz12332434sak
    otherapp:AAC456:yzf834509234uvw

The provided AWS access keys should only grant the least possible permissions, i.e. the "s3:GetObject" action to the application's subfolder in the Mint S3 bucket.
An example IAM policy might look like:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject"
                ],
                "Resource": "arn:aws:s3:::mint-example-bucket/myapp/*"
            }
        ]
    }

