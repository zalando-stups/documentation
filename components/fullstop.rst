.. _fullstop:

========
Fullstop
========

The latest documentation is available in the `Fullstop github project`_ page.

Fullstop Aws overview
.. image:: images/fullstop.png
Fullstop Architecture overview
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

.. _cross-account role: http://docs.aws.amazon.com/IAM/latest/UserGuide/roles-walkthrough-crossacct.html
.. _Fullstop github project: https://github.com/zalando-stups/fullstop
