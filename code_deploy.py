import boto3
from log import *

logger = setup_logger()

class CreateCodeDeploy:
    def __init__(self):
        logger.info('Creating boto3 session with environment variables')
        self.session = boto3.Session()
        logger.info('Boto3 session created successfully')

    def create_application(self):
        cd_client = boto3.client('codedeploy')
        logger.info('*** Creating new application ***')
        try:
            response = cd_client.create_application(
                applicationName='test_application',
                computePlatform='Server'
            )
            logger.info('Application created successfully')
            print('Response {}'.format(response))

        except:
            print('!!! Some error occured. Make sure the application name doesn''t exist already !!!')

        logger.info('*** Creating new deployment group ***') 
        try:     
            response_dg = cd_client.create_deployment_group(
                applicationName='test_application',
                deploymentGroupName='test_deployment_group',
                serviceRoleArn='arn:aws:iam::302536458080:role/mycodedeplyrole',
                ec2TagSet={
                    'ec2TagSetList': [
                        [
                            {
                                'Key': 'Name',
                                'Value': 'Code_Deploy_Server',
                                'Type': 'KEY_AND_VALUE'
                            }
                        ]
                    ]
                }  
            )
            logger.info('Deployment group created successfully')
            print('Response: {}'.format(response_dg))
        except:
          print('!!! Some error occured. Make sure the group name is not taken')

        logger.info('*** Creating new deployment ***')
        response_deployment = cd_client.create_deployment(
            applicationName='test_application',
            deploymentGroupName='test_deployment_group',
            revision={
                'revisionType': 'GitHub',
                'gitHubLocation': {
                    'repository': 'amansoni369/aws_infra',
                    'commitId': 'ef51e050dcffe066ff33cd48ac46706f10b57a90'
                 }
            }
        )
        logger.info('Deployment successfully created')
        print('deployment response:'.format(response_deployment))

