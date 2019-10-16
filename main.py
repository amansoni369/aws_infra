import boto3
import argparse
from aws_infra import *

def main():
# parse command line options
    parser = argparse.ArgumentParser()
    parser.add_argument('instance_type',
                        help='the type of instance',
                        type=str)
    parser.add_argument('key_name',
                        help='account key',
                        type=str)
    parser.add_argument('ami_id',
                        help='AMI id for instance',
                        type=str)
    
    parser.set_defaults(func=CreateInfrastructure)
    args = parser.parse_args()
    create_infra = CreateInfrastructure()
    infra_list = create_infra.create_network()
    instance_id = create_infra.create_instances(infra_list[0], infra_list[1], args)
    # create_infra.create_alarm(instance_id)     
        
if __name__ == "__main__":
    main()