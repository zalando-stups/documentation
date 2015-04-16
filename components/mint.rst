.. _mint:

====
Mint
====

**Mint** is STUPS' secret distributor and rotator. Its main task is to constantly rotate service passwords or API keys
and provide the secrets to the actual applications.

How it works
============

.. image:: mint/architecture.svg

Step 1 + 2
----------

At first, mint makes sure, that for every registered application has an own 'service user' in the IAM solution. It then
also deletes all users that are either inactive or do not even exist in Kio.

Step 3 + 4
----------

mint will regularly rotate the passwords and OAuth 2.0 credentials for all service user's. The new secrets are then
stored in an S3 bucket where each registered application has one directory. mint creates cross-account permissions for
all the directories and links them with the owner's AWS accounts.

Step 5
------

Applications can download their current secrets from their directory on S3 using their cross-account IAM role. It is now
the application owner's responsibility to assign the correct IAM profiles to the actual EC2 instances. :ref:`berry` can
help with the permanent retrieval of the application's secrets.

API for applications
====================

mint stores all credentials of an application in a directory in S3. At first, you have to know in which S3 bucket mint
stores everything. Knowing that, you can construct the correct URL to it:

    https://mints-s3-bucket.amazonaws.com/my-app-id/credentials.json

    <s3 bucket> / <app-id> / credentials.json

You should download the file via the AWS SDKs but you could also construct the HTTP request yourself according to the
Amazon documentation. The file contains the following content:

.. code-block:: json

    {
        "application_username": "abc",
        "application_password": "xyz",
        "client_id": "foo",
        "client_secret": "bar"
    }

The application username and password are the application's credentials for their own service user in your IAM solution.
The client ID and secret are the application's OAuth 2.0 credentials.

Look at :ref:`berry` for automated download of this file for your application. Remember that this file changes
regularly.
