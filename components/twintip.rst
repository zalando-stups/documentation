.. _twintip:

=======
TWINTIP
=======

**TWINTIP** is STUPS' API crawler.

TWINTIP collects API definition of all applications that are registered in Kio. In order to collect your API schema
TWINTIP requires your application to expose the following HTTP endpoint:

    https://myapp.example.com/.well-known/schema-discovery

This endpoint has to return the following JSON discovery document:

.. code-block:: json

    {
        "schema_url": "/swagger.json",
        "schema_type": "swagger-2.0",
        "ui_url": "/ui/"
    }

* The **schema_url** can be a relative path or full URL to the schema's definition file.
* The **schema_type** is the type of definition to expect from the schema_url. Only well supported currently is 'swagger-2.0'.
* The **ui_url** is optionally and can point to a human-friendly UI with which you can discover the API in more detail, like a Swagger UI.

TWINTIP will regularly visit your discovery endpoint and check for updates.
