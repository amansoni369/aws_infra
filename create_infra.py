import boto3
from log import *
from code_deploy import *

logger = setup_logger()

class CreateInfra:
    '''
    a simple class
    '''
    def __init__(self):
        '''
        init function to setup boto session
        '''
        logger.info('Creating boto3 session with environment variables')
        self.session = boto3.Session()
        logger.info('Session {} created'.format(self.session))

    def create_instance(self, ami_id, key_name):
        '''
        fucntion to launch ec2 istance
        '''
        ec2 = boto3.resource('ec2')
        logger.info('''Creating EC2 instance''')
        instance = ec2.create_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName=key_name,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'Code_Deploy_Server'
                        }
                    ]
                }
            ]
        )
        # check if ec2 instance is up and running
        logger.info('Check if ec2 instance is up and running')
        for instances in instance:
            instances.wait_until_running()
            ec2_client = boto3.client('ec2')
            instance_info = ec2_client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': ['running', 'pending']
                    }
                ]
            )
            instance_id = ''
            for reservations in instance_info['Reservations']:
                for instance in reservations['Instances']:
                    instance_id = instance['InstanceId']

        logger.info('INFO !! ec2 instance {0} is up and running'.format(instance_id))

if __name__ == "__main__":
     create_infra = CreateInfra()
     create_infra.create_instance('ami-0f767afb799f45102', 'sydney_new')

#     code_deploy = CreateCodeDeploy()
#     code_deploy.create_application()
