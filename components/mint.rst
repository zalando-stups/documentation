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
