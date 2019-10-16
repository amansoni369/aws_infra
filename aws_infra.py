import boto3
import argparse

class CreateInfrastructure:
    def __init__(self):
            print('Creating boto3 session with environment variables')
            self.session = boto3.Session()
            print('Session created: {}'.format(self.session))
        
            
    def create_network(self):
        client = self.session.client('ec2')
        ec2 = boto3.resource('ec2')
    
    # creating VPC
        print('... creating vpc ...')
        vpc_response = client.create_vpc(
            CidrBlock='172.31.0.0/16'
            )
        vpc_id = vpc_response['Vpc']['VpcId']
    # checking if vpc is created or not
        while vpc_id is None:
            continue
        else:
            print('VPC {0} created successfully ...'.format(vpc_id))
              
    # Creating internet gateway
        response_ig = client.create_internet_gateway()
        igw_id = response_ig['InternetGateway']['InternetGatewayId']
    # attaching internet gateway to vpc
        response_attach_ig = client.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )

    #  creating route table and adding routes
        create_route_response = client.create_route_table(
            VpcId=vpc_id
            )
        route_table_id = create_route_response['RouteTable']['RouteTableId']

        #vpc = ec2.Vpc(vpc)
        print('... creating subnet to launch ec2 instances ...')
        subnet = client.create_subnet(
            CidrBlock='172.31.0.0/24',
            VpcId=vpc_id
        )
        subnet_id = subnet['Subnet']['SubnetId']
        while subnet_id is None:
            continue
        else:
            print('SUBNET {0} created successfully ...'.format(subnet_id))

    # modifying subnet properties to assign ip address while instance creation
        print('.. modifying subnet to match public ip to server on launch ...')
        associate_ip = client.modify_subnet_attribute(
            MapPublicIpOnLaunch={
                'Value': True
            },
            SubnetId=subnet_id
        )
        
    # associating route table with subnet
        association_response = client.associate_route_table(
            RouteTableId=route_table_id,
            SubnetId=subnet_id
            )
        
    # add route to igw
        response = client.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=igw_id,
            RouteTableId=route_table_id
            )
    # create security group to allow only ssh to the ec2 instance
        print('... creating security group for ec2 ...')
        response_sg = client.create_security_group(
            Description='Security Group to allows incoming ssh traffic to an ec2 isntance',
            GroupName='AllowSSH',
            VpcId=vpc_id
        )
        sg_id = response_sg['GroupId']

    # authorize security group ingress rules
        response_sg_rule = client.authorize_security_group_ingress(
            CidrIp='0.0.0.0/0',
            FromPort=22,
            GroupId = sg_id,
            IpProtocol='TCP',
            ToPort=22
        )
        return [subnet_id, sg_id]


## Create ec2 instance in the above created infra
    def create_instances(self, subnet_id, sg_id, args):
        ec2 = boto3.resource('ec2')
        print('... creating ec2 instances ...')
        instance = ec2.create_instances(
            ImageId = args.ami_id,
            MinCount = 1,
            MaxCount = 2,
            InstanceType = args.instance_type,
            KeyName = args.key_name,
            SubnetId = subnet_id,
            SecurityGroupIds=[sg_id]
        )
        # checking if ec2 instance is up and running
        print('... waiting for instances to be up and running ...')
        for instances in instance:
            instances.wait_until_running()
        ec2_client = boto3.client('ec2')
        instance_information = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running','pending']
                    }
            ]
        )
        instance_id=[]
        for reservation in instance_information['Reservations']:
            for instance in reservation['Instances']:
                instance_id.append(instance['InstanceId'])
        print('INFO!! ec2 instance(s) {0} up and running'.format(instance_id))

        return instance_id


    # Create CloudWatch client
    '''def create_alarm(self, instance_id):
        cloudwatch = boto3.client('cloudwatch')
        # Create alarm
        for instances in instance_id:
            print('... setting up alarm for {} ...'.format(instances))
            cloudwatch.put_metric_alarm(
                AlarmName='Monitor_CPU_Utilization',
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=1,
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Period=60,
                Statistic='Average',
                Threshold=80.0,
                ActionsEnabled=False,
                AlarmDescription='Alarm when server CPU utilization exceeds 80%',
                Dimensions=[
                    {
                    'Name': 'InstanceId',
                    'Value': instances
                    },
                ],
                Unit='Seconds'
                )
            cloudwatch.put_metric_alarm(
                AlarmName='Monitor_Network',
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=1,
                MetricName='NetworkIn',
                Namespace='AWS/EC2',
                Period=60,
                Statistic='Average',
                Threshold=500000,
                ActionsEnabled=False,
                AlarmDescription='Alarm when server CPU utilization exceeds 80%',
                Dimensions=[
                    {
                    'Name': 'InstanceId',
                    'Value': instances
                    },
                ],
                Unit='Seconds'
                )
        print('ALARM created successfully')
    '''
