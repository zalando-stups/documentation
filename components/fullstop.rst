.. _fullstop:

=========
fullstop.
=========

The latest documentation is available in the `Fullstop github project`_ page.

fullstop. AWS overview

.. image:: images/fullstop.png

fullstop. Architecture overview

.. image:: images/fullstop-architecture.png

Aim of the project is to enrich CloudTrail log events.

In our scenario we have multiple AWS accounts that need to be handled.

Each of this account has CloudTrail activated and is configured to write
in a bucket that resides in the account where also fullstop is running.
(Right now in AWS it's not possible to read CloudTrail logs from a different account)

Fullstop will then process events collected from CloudTrail.

To enrich CloudTrail log events with information that comes
from other systems than AWS, we should only configure fullstop to do so.

Fullstop can even call the AWS API of a different account, by using a `cross-account role`_.
The account that is running fullstop should therefore be trusted
by all other accounts in order to perform this operations.

.. image:: images/fullstop-cross-account-role.png

Command Line Client
===================

Fullstop comes with a convenience command line client:

.. code-block:: bash

    $ sudo pip3 install --upgrade stups

First configure your Fullstop CLI for your AWS account IDs:

.. code-block:: bash

    $ fullstop configure
    # enter Fullstop URL and your AWS account IDs

For example, you can list all recent violations in your configured AWS accounts:

.. code-block:: bash

    $ fullstop list-violations --since 7d -l 50

Resolving Violations
--------------------

You can resolve batches of violations with the ``resolve-violations`` command which has similar
filtering/matching options as ``list-violations``.

.. code-block:: bash

    $ fullstop resolve-violations -t <VIOLATION-TYPE> -l 100 --since 7d '<comment>'

Filtering by applications / versions is also possible. Multiple values must be comma-separated:

.. code-block:: bash

    $ fullstop resolve-violations -t <VIOLATION-TYPE> --applications my-app --application-versions 1.0,1.1 '<comment>'

Parts of the meta field can also be matched for more finegrained control, for example:

.. code-block:: bash

    $ fullstop resolve-violations -t WRONG_AMI -m ami_name=another-ami 'My boss wants me to do this'


.. _cross-account role: http://docs.aws.amazon.com/IAM/latest/UserGuide/roles-walkthrough-crossacct.html
.. _Fullstop github project: https://github.com/zalando-stups/fullstop
