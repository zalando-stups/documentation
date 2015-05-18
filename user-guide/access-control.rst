.. _access-control:

==============
Access Control
==============

The STUPS ecosystem integrates via OAuth 2.0 into your IAM solution and also provides first-class support for deploying
applications that support OAuth 2.0. This document gives you an overview of OAuth 2.0 concepts, how they are integrated
into the STUPS ecosystem and how you integrate them into your own application.

------------------
OAuth 2.0 concepts
------------------

.. image:: access-control/oauth2.png

OAuth 2.0 is a security standard, that focuses on the delegation of permissions. With some conventions it can also
provide authentication and authorization for you. To understand OAuth, you need to understand the 4 basic roles that
take part in OAuth flows:

Resource Owner
--------------

The resource owner is typically a human (but doesn't have to be) that owns a resource (data). The resource owner should
be the only one, who can grant access to his resources.

A typical resource owner is a customer, who is owner of his orders in a shop. Only he should decide, who can access his
order information. Another example is an employee who owns his salary information.

A resource owner is everything, that can authenticate with the authorization server. This can include other services
too.

Resource Server
---------------

A resource server is a service, that stores data of resource owners and has to protect them. It is typically a REST CRUD
API, that provides access to certain information. The resource server will deny every access to a resource as long as it
does not get a valid proof, that the resource owner allows the access. Resource server mostly don't have much logic
besides validation.

Client
------

A client is a tool or service, that a resource owner wants to use to read or modify his resources. In order to get
access to the resource owner's resource, the client can ask the resource owner for his consent. If the resource owner
gives his consent, the client will get a proof that it can forward to the resource server in order to access the
resource. Clients contain some business logic which requires access to resources. They should themself not require
any permission checks.

Authorization Server
--------------------

The authorization server is the central trusted authority of your ecosystem, which can authenicate resource owners,
manage the delegation process and validate that permission delegations are valid.

Roles Overview
--------------

.. image:: access-control/roles.svg

TODO: grant types w/ flows, links to further documentation, roles can mix in one application

--------------
STUPS concepts
--------------

STUPS works with a mental model around data access control. When defining access control, you have to think about
access to data instead of access to actions. This way of thinking about access control nicely aligns with RESTful
services as you always talk about data instead of the SOAP way of thinking, where you define everything in actions.

:ref:`essentials` is STUPS' microservice that stores data about all your permission. It has the notion of resource
types and scopes.

Resource Types
--------------

Resource types are a categorization of your resources. A typical resource type might be a "sales order" or
"creditcard". The actual resource will then later be an actual creditcard or sales order.

Resource types define, who can own resources of this type. This is typically one user group like "customers" but
can also be multiple ones like "customers" and "employees". It is also possible to define no resource owner at all
for resources, that you just cannot locate in any user group like article information about shoes.

Scopes
------

Scopes define the type of access permission you have to a resource. They are always bound to a resource type. You
can define scopes like "creditcard.read" and "creditcard.write", symbolizing read or write access to creditcard
information. Since in the real world, we cannot always ask the resource owner to grant us his permission to access
his resource, we have to distinguish between permissions that a resource owner can grant and permissions, that
special applications can obtain.

Resource Owner Scopes
---------------------

The resource owner scope should always be the default choice. Permissions of this type can automatically be granted
by the resource owner to clients. Those are typically scopes like "sales_order.read" or "sales_order.write" that
grant read or write access to a resource. Those scopes always have to be evaluated in the context of the resource
owner by the resource server. This means, the resource server has to check if permission for access was granted
and that the requested resource is really owned by this particular resource owner.

Application Scopes
------------------

The opposite of resource owner scopes are application scopes, which are not bound to the context of the resource
owner. Typical applications scopes look like "sales_order.read_all" and are used by batch jobs that may do
analytics on them. By default, no one can grant this scope and you have to assign your application this
permission explicitly.

--------------------
STUPS infrastructure
--------------------

STUPS supports you to use OAuth 2.0 by handling secret distribution and access control management for you.
:ref:`mint` & :ref:`berry` will automatically create service users for your registered applications in
:ref:`kio` and send their passwords to your AWS account. mint will also create client configurations for
your applications that you will need in order to ask for permission. :ref:`essentials` store all basic
information about possible access permissions.

-----------------------
Application integration
-----------------------

The following sections will give you a detailed technical introduction of how to implement the important OAuth 2.0
roles with your application. You either implement a resource server or a client, depending on what you want to
do. Those roles are strictly separated in their part the play in access control. This does not necessarily mean,
that your application itself only implements one role. Depending on your use cases, some flows require your
application to be a client, some require it to act as a resource server.

In the next steps, we will implement the handling of "sales orders" data in your ecosystem. Sales order data
might be owned by customers and employees. We want to distinguish read and write access and we also need
a batch job, that analyses all the orders.


Helpful tooling
---------------

Before starting to integrate OAuth 2.0 in your application, you should install :ref:`zign`. Zign is a
command line tool, that allows you to easily create OAUth 2.0 access tokens for yourself. This is especially
helpful for testing resource servers.

.. code-block:: bash

    $ sudo pip3 install --upgrade stups-zign

With the following command, you can generate an access token for yourself with all the scopes you specify:

.. code-block:: bash

    $ zign token creditcard.read creditcard.write

You can name tokens, so that you can access them repeatedly without authenticating again every time:

.. code-block:: bash

    $ zign token -n testing creditcard.read creditcard.write
    $ zign list
    $ zign token -n testing


Preparation of global meta data
-------------------------------

Before integrating your application, you need to publish the basic metadata about your data in your ecosystem. This has
to be done via the :ref:`essentials` microservice (which can be accessed via :ref:`yourturn`).

We define the following new resource type:

* ID: **sales_order**
* Name: sales order
* Resource Owners:
    * [x] Employees
    * [x] Customers

For this resource type, we define the following scopes:

* sales_order.read
    * ID: **read**
    * Summary: grants read access
    * [x] Resource Owner Scope
* sales_order.write
    * ID: **write**
    * Summary: grants write access
    * [x] Resource Owner Scope
* sales_order.read_all
    * ID: **read_all**
    * Summary: grants read access to all orders
    * [x] Application Scope

With this information published, everyone can now check based on those permissions.

Implementing a resource server
------------------------------

If you are storing data, you are a resource server and have to protect those data. Luckily, this is the easiest role
in the OAuth 2.0 flows. The requirements are pretty simple: you need to enforce that you get an access token, you have
to validate the access token and authorize the access based on the information of the access token.

Execute the following commands to simulate a resource server:

.. code-block:: bash

    $ TOKEN=$(zign token uid)
    $ curl "https://auth.example.com/oauth2/tokeninfo?access_token=$TOKEN"

Your output should look like the following JSON:

.. code-block:: json

    {
      "expires_in": 3515,
      "token_type": "Bearer",
      "realm": "employees",
      "scope": [
        "uid"
      ],
      "grant_type": "password",
      "uid": "yourusername",
      "access_token": "4b70510f-be1d-4f0f-b4cb-edbca2c79d41"
   }

In you application, you need to get the access token from the HTTP Authorization header. The authorization header should
look like the following example:

.. code-block:: text

    Authorization: Bearer 4b70510f-be1d-4f0f-b4cb-edbca2c79d41

If the header is not set, return a 401 status code to signal, that you require an access token.

Using this access token as above to query the "tokeninfo" endpoint will return the token's associated session
information. In general, everyone can take an access token and ask the "tokeninfo" endpoint to send back
the session information. Asking for this information as a resource server already solves the first
of your two steps: if the token is invalid, you won't get back this information. The second step is now custom logic
on your site: interpreting the result.




Implementing a client: Asking resource owners for permission
------------------------------------------------------------

Implementing a client: Using own permissions
--------------------------------------------

