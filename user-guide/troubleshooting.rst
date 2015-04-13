===============
Troubleshooting
===============

I cannot access my EC2 instance via SSH
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you can get access to :ref:`odd` via :ref:`piu`, but accessing your private EC2 instance does not work: First check your server's security group. It must allow inbound traffic on TCP port 22 (SSH).
