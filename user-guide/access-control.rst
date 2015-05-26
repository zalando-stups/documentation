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

`OAuth 2.0 is a security standard`_, that focuses on the delegation of permissions. With some conventions it can also
provide authentication and authorization for you. To understand OAuth, you need to understand the 4 basic roles that
take part in OAuth flows:

.. _OAuth 2.0 is a security standard: http://oauth.net/2/

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

The authorization server is the central trusted authority of your ecosystem, which can authenticate resource owners,
manage the delegation process and validate that permission delegations are valid.

Roles Overview
--------------

.. image:: access-control/roles.svg

Abstract OAuth 2.0 Flow
-----------------------

This is not a real flow but should give you a basic understanding of how OAuth works. In this example, a shoe search
application can search for shoes for a customer and add them to the customer's wishlist. The customer is obviously
the resource owner of her wishlist. We also have a wishlist service that stores the customer's wishlist, which
is the resource server and the shoe search application is the client who wants to store shoes on behalf of the
customer.

#. The customer searches for new shoes in the show search application and finds a new pair. The customer clicks on
   the "save in my wishlist" button.
#. The shoe search application will now redirect the customer to the customer's authorization server with the
   information to which page to come back if the customer authorized the action. The shoe search application also
   transmits which scopes it needs. Think of scopes as "permission to access a certain set of a resource's data" - in this case it transmits the "whishlist.write" scope.
#. The customer will land on the login screen of his authorization server, put in her password and agree, that the
   shoe search application can have the "wishlist.write" scope. After agreeing, the authorization server will
   redirect the customer back to the previously submitted page of the shoe search application, including a proof,
   that the customer agreed.
#. The shoe search application can now take the proof and submit it along with the "store wishlist" call to the
   wishlist service. 
#. The wishlist service can take the submitted proof and validate it by sending it to the authorization server.
   If the authorization server confirms the validity of the proof, the wishlist service can go on and store the
   shoe in the customer's wishlist.

Which role has my application?
------------------------------

Actually, your application can fulfill every role. It can be a resource server, a client and also a resource owner.
It is also not unlikely, that your application fulfills multiple roles at once. For example, for service-to-service
authorization, where no human can be involved, your application will be resource owner and client at once in order
to create access tokens for itself. You should always try to be a client only and only work with delegated
permissions as that frees you have doing authorization of any kind on your own or handling credentials.

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
"creditcard". The actual resource will then later be an actual credit card or sales order.

Resource types define, who can own resources of this type. This is typically one user group like "customers" but
can also be multiple ones like "customers" and "employees". It is also possible to define no resource owner at all
for resources, that you just cannot locate in any user group like article information about shoes.

Scopes
------

Scopes define the type of access permission you have to a resource. They are always bound to a resource type. You
can define scopes like "creditcard.read" and "creditcard.write", symbolizing read or write access to credit card
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

With this information published, every resource server can now grant access based on those permissions.

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

If the header is not set, return a 401 status code to signal that you require an access token. Consult the `Bearer Token RFC <https://tools.ietf.org/html/rfc6750#section-3.1/>`_ for a detailed explanation of what errors should look like and what status code you should return.

Using this access token as above to query the "tokeninfo" endpoint will return the token's associated session
information. In general, everyone can take an access token and ask the "tokeninfo" endpoint to send back
the session information. Asking for this information as a resource server already solves the first
of your two steps: if the token is invalid, you won't get back this information. The second step is now custom logic
on your site: interpreting the result.

In STUPS, we are using the convention, that every scope also has an associated attribute with the same name. This
means if you are requesting a "foobar" scope, the tokeninfo will contain an attribute "foobar: true" if the token
has the permission for foobar. Else the attribute might be false or non-existant. That way, the terms "permission"
and "scope" are somehow interchangeable.

Some pseudo code:

.. code-block:: java

    // check that token exists on the request
    if (request.getHeader("Authorization") == null) {
      // return 401 without error information
      throw new UnauthorizedException(401);
    }
    // get token from authorization header of incoming request
    token = request.getHeader("Authorization").substring("Bearer ".length());

    // get tokeninfo and check if token is valid
    response = http.get("https://auth.example.com/oauth2/tokeninfo?access_token=" + token);
    if (response.status != 200) {
        throw new UnauthorizedException(401, "invalid token");
    }

    // check if the permission is actually true
    tokeninfo = response.body;
    if (tokeninfo.get("write_access") != true) {
        throw new UnauthorizedException(403, "you lack the required permission");
    }

    // check if accessing owners resource
    if (tokeninfo.get("uid") != resource.owner) {
        throw new UnauthorizedException(403, "the requested resource does not belong to you");
    }

    // finally, the token is valid, it has the write permission and the resource really
    // belongs to the user, execute request
    write(resource, requestt);


Implementing a client: Asking resource owners for permission
------------------------------------------------------------

Client implementations are the hardest part in OAuth 2.0. We really encourage you to use an existing library for
your programming language - there are plenty of them. There are three commonly used grant types (grant types
are a synonym for flows):

#. `Authorization Code Grant`_
    * This should be the default whenever you want to implement a client. It is the most secure way to do OAuth 2.0.
      You will need a client ID and a client secret to use this grant type. When you get your credentials via
      :ref:`mint`, you will also get these client credentials in the "client.json".
#. `Implicit Grant`_
    * This grant type is meant for situations, where you are not in control of the client's environment and it is
      de facto untrusted. This is primarily the case for JavaScript only web apps or mobile applications. In both cases
      does the client code reside on a foreign device. Therefor the client code and configuration is not secret.
      This grant type should only be used in those two cases. Try to use the Authorization Code Grant whenever
      possible. As the configuration cannot be considered secure, your client will also only require a client ID
      and not a client secret.
#. `Resource Owner Password Credentials Grant`_
    * There are only two use cases for the password grant. The password grant enables a client to use the resource
      owner's password directly to create tokens with it. This means, that your client really has to get the password
      of the owner - the main case you want to avoid normally with OAuth.
        * The first use case of the password grant is around user convenience. Especially non technical people will
          get scared and lose trust if they get redirected to other pages to enter their passwords. Especially in
          a shop environment, you do not want to loose conversion rate by disturbing the user experience. It is
          also not desirable to ask a customer to grant some permissions. In this case, a shop frontend can act
          as the customer on behalf of him. The frontend will ask and get the password of the customer and can then
          create tokens on behalf of her. As the user's password will get into the hands of your application, this
          should be avoided as much as possible because you also have to duplicate all the security measurements
          again that are also done in your authorization server.
        * The second use case is using service users as resource owners. See the next topic about using own
          permissions.

.. _Authorization Code Grant: https://tools.ietf.org/html/rfc6749#section-4.1
.. _Implicit Grant: https://tools.ietf.org/html/rfc6749#section-4.2
.. _Resource Owner Password Credentials Grant: https://tools.ietf.org/html/rfc6749#section-4.3

Implementing a client: Using own permissions
--------------------------------------------

STUPS support service-to-service authorization via OAuth 2.0. This is useful in batch jobs, where you do not
have the possibility to ask the resource owner for permission to access his data. This means, that your application
itself has to somehow authenticate itself, so that a resource server can grant access. For this, :ref:`mint` will
automatically create service users for you. These service users have an own identity and also an own username and
password that you can read in your "user.json". You can assign this user permissions via :ref:`yourturn`. A
typical permission would look like "sales_order.read_all".

Via the previously mentioned "password grant" can you now create access tokens for yourself with your own
credentials and permissions. Instead of complex redirect flows like with humans, it is very simple to create a
token if you have the password of the resource owner (yourself in this case):

.. code-block:: bash

    $ cat > request.json << "EOF"
    {
        "grant_type": "password",
        "username": "my-username",
        "password": "my-password",
        "scope" "uid sales_order.read_all"
    }
    EOF

    $ curl -X POST -u my-client-id:my-client-secret -d @request.json \
        "https://auth.example.com/oauth2/access_token?realm=services"

You will get back an access token that will result in the following tokeninfo if you check it:

.. code-block:: json

    {
      "expires_in": 3515,
      "token_type": "Bearer",
      "realm": "services",
      "scope": [
        "uid",
        "sales_order.read_all"
      ],
      "grant_type": "password",
      "uid": "my-username",
      "sales_order.read_all": true,
      "access_token": "4b70510f-be1d-4f0f-b4cb-edbca2c79d41"
   }

That way, you can create access token for your own service user and access other applications with it. If you
look carefully at the request JSON, you will see, that you also provide the scopes, that should actually be in
the token. That way, you can create tokens with the minimal set of permissions that you delegate. It is a good
practice to create custom tokens per use case, so that you never expose more permissions than are actually required.
