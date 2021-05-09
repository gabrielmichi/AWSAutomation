##Backup Simples criado na aula de BOTO3 - Curso Cloud Ninja

import json
import boto3

def lambda_handler(event, context):
    
    
    ec2_client = boto3.client('ec2')

    regions = ec2_client.describe_regions()

    for region in regions['Regions']:
            ec2_client = boto3.client('ec2', region_name=region['RegionName'])
            volumes = ec2_client.describe_volumes()
            
            for volume in volumes['Volumes']:
                volumeid=volume['VolumeId']
                size=volume['Size']
                state=volume['State']
                volumetype=volume['VolumeType']
                
                print("%s,%s,%s,%s" %(volumeid,size,state,volumetype))