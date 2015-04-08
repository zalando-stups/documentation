===================
Amazon Web Services
===================

General guiding principles:

* Team is the main entity for ownership and security boundaries.
* Interactions between teams (e.g. service calls) should involve the minimum friction possible.
* Sensitive data (e.g. customer data) must only be accessible by authorized personnel.
* All deployed software components must have sane default security settings.

Every team gets their own AWS account with defacto-administrator access to all resources in it:

* This ensures that only team members can manage their AWS resources.
* Team members use the AWS infrastructure by authenticating via SAML
* Teams are fully responsible for all data that is processed in their AWS account.
* All running applications (exposing HTTPS) are automatically available to other teams.

.. toctree::
   :maxdepth: 1

   saml
   zalando-ami
   best-practice
   audit
