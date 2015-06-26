=======
Storage
=======

For stateful applications with persistent storage, you can use:

* EBS volumes
* EC2 instance storage

Using EBS Volumes
=================

Initialize a new Senza definition YAML, e.g. for the "hello-world" app:

.. code-block:: bash

    $ senza init hello-world.yaml

Create an EBS volume with a unique "Name" tag, e.g. "my-volume":

.. code-block:: bash

    $ aws ec2 create-volume --availability-zone eu-west-1 --size 2 # GiB
    {
        "Size": 2,
        "Encrypted": false,
        "SnapshotId": "",
        "CreateTime": "2015-06-26T11:30:30.200Z",
        "AvailabilityZone": "eu-west-1a",
        "VolumeId": "vol-12345678",
        "VolumeType": "standard",
        "State": "creating"
    }
    $ aws ec2 create-tags --resources vol-12345678 --tags Key=Name,Value=my-volume


Add the needed IAM policy to allow attaching the EBS volume:

.. code-block:: bash

    PERMISSIONS_POLICY=/tmp/policy
    cat << EOF > "$PERMISSIONS_POLICY"
    {
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:AttachVolume",
                "ec2:DetachVolume"
            ],
            "Resource": "*"
        }
    }
    EOF

    aws iam put-role-policy --role-name "app-hello-world" \
        --policy-name "AllowUsingEBS" --policy-document "file://$PERMISSIONS_POLICY"

Change the Senza definition ("hello-world.yaml") to mount the EBS volume:

* Add "AvailabilityZones: [eu-west-1a]" below "Type: Senza::StupsAutoConfiguration"
* Add "volumes" and "mounts" below the "TaupageConfig" section

The resulting Senza definition YAML might look like:

.. code-block:: yaml

    SenzaComponents:
      - Configuration:
          Type: Senza::StupsAutoConfiguration
          AvailabilityZones: [eu-west-1a] # use EBS volume's AZ

      - AppServer:
          Type: Senza::TaupageAutoScalingGroup
          # ...
          TaupageConfig:
            runtime: Docker
            source: "..."
            # ...
            volumes:
              ebs:
                /dev/sdf: my-volume
            mounts:
              /data:
                partition: /dev/xvdf


.. Note::

    You either need to format the EBS volume manually the first time or use the "erase_on_boot" Taupage option.

