.. _even:

====
even
====

**even** allows requesting SSH access to EC2 instances.

How to use
==========

See the section :ref:`ssh-access` on how to get SSH access to EC2 instances using the :ref:`piu` command line tool.

SSH access granting flow
========================

This section explains how :ref:`piu`, :ref:`even`, :ref:`odd` and the IAM services (OAuth2 provider, Team Service and User Service) interact during the process
of granting SSH access to a single odd SSH bastion host.

.. image:: images/grant-ssh-access-flow.svg
   :alt: SSH access granting flow

#. user "jdoe" gets OAuth2 access token from Token Service (done by :ref:`piu`)
#. user "jdoe" requests access to a specific :ref:`odd` SSH bastion host "odd.myteam.example.org" (HTTP POST to /access-requests, done by :ref:`piu`)
#. even authenticates the user by retrieving the "uid" ("jdoe") from the OAuth2 tokeninfo endpoint
#. even authorizes the user "jdoe" by checking the team membership (member of "myteam") and comparing the requested hostname ("odd.myteam.example.org) to the configured hostname template
#. even executes the SSH forced command "grant-ssh-access jdoe" on the odd host
#. the odd host downloads the user's public SSH key from even (GET /public-keys/jdoe/sshkey.pub)
#. even retrieves the user's public SSH key from the configured user service (simple HTTP endpoint to get public SSH key by username)
#. the forced command on odd adds the user "jdoe" to the system and writes the ``authorized_keys`` file
#. the user "jdoe" finally logs into the odd host using his personal SSH key

