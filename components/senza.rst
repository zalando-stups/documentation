.. _senza:

=====
Senza
=====

**Senza** is STUPS' deployment tool.

See the :ref:`deployment` section for details on how to deploy applications using Senza, :ref:`pierone` and :ref:`taupage`.

Creating Stacks
===============

.. code-block:: bash

    $ senza create myapp.yaml 1 0.1-SNAPSHOT

Listing Stacks
==============

.. code-block:: bash

    $ senza list myapp.yaml       # list only active stacks for myapp
    $ senza list myapp.yaml --all # list stacks for myapp (also deleted ones)
    $ senza list                  # list all active stacks
    $ senza list --all            # list all stacks (including deleted ones)

Deleting Stacks
===============

.. code-block:: bash

    $ senza delete myapp.yaml 1
