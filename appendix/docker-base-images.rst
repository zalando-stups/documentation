.. _docker-base-images:

==================
Docker Base Images
==================

All Zalando Docker images include the Zalando CA and use immutable tags,
i.e. each new image version will increment the Docker tag version.

========= ===========
Name      Description
========= ===========
Ubuntu_   Ubuntu base image
OpenJDK_  Java 8 base image (Zalando CA is imported into Java TrustStore)
Python_   Python 3.4 base image
Node.js_  Node.js base image
========= ===========

.. _Ubuntu: https://github.com/zalando/docker-ubuntu
.. _OpenJDK: https://github.com/zalando/docker-openjdk
.. _Python: https://github.com/zalando/docker-python
.. _Node.js: https://github.com/zalando/docker-node

