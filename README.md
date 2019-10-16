**main_ref.py**
-----------
This script creates network required to launch an ec2 instance. It creates a VPC, Internet gateway, route tables, subnet. Once network is created we can launch the ec2 instance in the created subnet

Pre-Requisites
------------------

Configure aws environment variable of the aws account you want to run the script in as the code uses boto3 to set up session.

Running the Script
------------------------

The script requires a few command line arguments namely 

* `instance type`: to specify the instance type you want to launch
* `ami_id`: AMI id of the instance
* `key`: key name required to connect to the server later

Result
-------------

Once script is run, you are ready to use your ec2 instance. You can check it by logging in using putty or terminal

Dependencies
-------------

No Dependencies

Author
----------

amansoni369@gmail.com - Aman Soni


**setup_aws_infra.yml**
---------------------
