.. _key-encryption:

==============
Key Encryption
==============

Would you like to encrypt your password or other sensitive configurations?

This procedure is the same for all passwords (DB, log provider, ...) you will encrypt.

* Login into AWS console.
* Open the IAM service.
* Click on Role and find the name of your application role (normally app-<application-name>). NOTE: If there is no role for your application, this can be generated for you by ``senza`` when running ``senza init``.
* Now go back, or click on the left hand side on encryption keys.

.. Caution::

    Select the right region!

* Click on create key
* Add an alias and a description
* Next step
* For key administrator add Shibboleth-PowerUser and remove the key deletion option
* Next step
* For key usage permission add Shibboleth-PowerUser and the role name of your app (normally app-<application-name>)
* Now you are done!

You will see that your key get's an ARN (Amazon resource name):

.. code-block:: bash

    arn:aws:kms:eu-west-1:<account-id>:key/<kms-key-id>

Now we can proceed with the encryption of our password:

Let's test if all works:

.. code-block:: bash

    # 1. Encrypt and save the binary content to a file:
    $ aws kms encrypt --key-id $KMS_KEY_ID --plaintext "<here-you-can-paste-your-pwd>"  --query CiphertextBlob --output text | base64 | tr -d '\n' > /tmp/encrypted

.. code-block:: bash

    # 2. Then feed this encrypted content back to decrypt.  Note that the Plaintext that comes back is base64 encoded so we need to decode this.
    $ echo "Decrypted is: $(aws kms decrypt --ciphertext-blob fileb:///tmp/encrypted  --output text --query Plaintext | base64 | tr -d '\n')"

If all works we can now repeat the first step without the base64 encoding:

.. code-block:: bash

    $ aws kms encrypt --key-id $KMS_KEY_ID --plaintext "<here-you-can-paste-your-pwd>"  --query CiphertextBlob --output text

and here is our encrypted password.

.. Important::

    You can use the :ref:`taupage` decryption functionality, that allows you to define in :ref:`senza` YAML your property as encrypted.
    Taupage will then decrypt the password for you and set the unencrypted value on the same property for your application.

    To do that define the value in the YAML as:

        .. code-block:: yaml

            my_secret: "aws:kms:<here-the-encryption-result>"
