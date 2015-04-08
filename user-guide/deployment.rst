==========
Deployment
==========

The :ref:`senza` command line tools allows deploying application stacks.

.. code-block:: bash

    $ pip3 install --upgrade stups-mai stups-senza

First deploy the application's artifact (Docker image) to :ref:`pierone`, e.g.:

.. code-block:: bash

    $ cd myapp # enter your application's source folder
    $ docker build -t pierone.stups.example.org/myteam/myapp:1.0 .
    $ docker push pierone.stups.example.org/myteam/myapp:1.0

Next you need to create a new deployment definition YAML file:

.. code-block:: yaml

    Description: "MyApp version {{Arguments.ImageVersion}}"

    # basic information for generating and executing this definition
    SenzaInfo:
      StackName: myapp
      Parameters:
        - ImageVersion:
            Description: "Docker image version of MyApp."

    # a list of senza components to apply to the definition
    SenzaComponents:

      # this basic configuration is required for the other components
      - Configuration:
          Type: Senza::StupsAutoConfiguration

      # will create a launch configuration and auto scaling group with scaling triggers
      - AppServer:
          Type: Senza::TaupageAutoScalingGroup
          InstanceType: t2.medium
          SecurityGroups:
            - sg-123123
          IamInstanceProfile: arn:aws:iam::123456789012:instance-profile/app-myapp
          ElasticLoadBalancer: AppLoadBalancer
          TaupageConfig:
            runtime: Docker
            source: myteam/myapp:{{Arguments.ImageVersion}}
            ports:
              8080: 8080
            notify_cfn:
              stack: "{{SenzaInfo.StackName}}-{{SenzaInfo.StackVersion}}"
              resource: "AppServer"
            environment:
              SOME_ENV: foobar
          AutoScaling:
            Minimum: 2
            Maximum: 10
            MetricType: CPU
            ScaleUpThreshold: 70
            ScaleDownThreshold: 40

      # creates an ELB entry and Route53 domains to this ELB
      - AppLoadBalancer:
          Type: Senza::ElasticLoadBalancer
          HTTPPort: 8080
          SSLCertificateId: arn:aws:iam::123456789012:server-certificate/myapp
          HealthCheckPath: /
          SecurityGroups:
            - sg-123123
          Domains:
            MainDomain:
              Type: weighted
              Zone: myteam.example.org
              Subdomain: myapp
            VersionDomain:
              Type: standalone
              Zone: myteam.example.org
              Subdomain: myapp-{{SenzaInfo.StackVersion}}


In order to create the Cloud Formation stack, we need to login with :ref:`mai`:

.. code-block:: bash

    $ mai create myteam # create a new profile (if you haven't done so)
    $ mai # login

Create the application's Cloud Formation stack with Senza:

.. code-block:: bash

    $ senza create definition.yaml --region=eu-west-1 1 1.0

.. Note:: The last parameter is a custom parameter "ImageVersion" defined in the SenzaInfo/Parameters section of the above definition YAML.

.. Tip:: You can avoid passing the ``--region`` option by configuring the default AWS region ID in ``~/.aws/config``. See the `AWS CLI docs`_ for details.

.. _AWS CLI docs: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
