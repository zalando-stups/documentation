==============
What is STUPS?
==============

The STUPS platform is a set of tools and components
to provide a convenient and audit-compliant Platform-as-a-Service (PaaS) for multiple autonomous teams
on top of Amazon Web Services (AWS).

STUPS provides the needed components to deploy immutable stacks of Docker applications on AWS:

* an **application registry** to register applications and their endpoints (:ref:`kio`)
* a private **Docker registry** to push deployment artifacts to (:ref:`pierone`)
* a CLI **tool to create temporary AWS credentials** when using federated SAML logins (:ref:`mai`)
* an **AWS account configuration tool** to setup team AWS accounts consistently (:ref:`sevenseconds`)
* a **base Amazon Machine Image (AMI)** to run Docker containers in a safe and audit-compliant way (:ref:`taupage`)
* a **developer console UI** to register and browse applications and their versions (:ref:`yourturn`)
* **tools to grant team members SSH access** to EC2 instances in an audit-compliant way (:ref:`piu` and :ref:`even` & :ref:`odd`)
* a **best practice CLI tool to deploy** immutable application stacks using AWS CloudFormation (:ref:`senza`)
* a **reporting component** to ensure compliance and transparency across all AWS team accounts (:ref:`fullstop`)
* a **framework for OAuth integration** via secret distribution (:ref:`mint` & :ref:`berry`)
