import json
import boto3

def lambda_handler(event, context):
    
    #colocar account ID da conta que estou utilizando
    myaccountid="569093484582"
    
    #IMAGES
    #Alterar a região
    for region in ['us-east-1','us-east-2']:
            ec2_client = boto3.client('ec2', region_name=region)
            images = ec2_client.describe_images(Owners=[myaccountid])
            for image in images['Images']:
                print(f'images, {image["ImageId"]},{image["CreationDate"]}')
    
    #SNAPSHOTS
    for region in ['us-east-1','us-east-2']:
            ec2_client = boto3.client('ec2', region_name=region)
            snapshots = ec2_client.describe_snapshots(OwnerIds=[myaccountid])
            
            for snapshot in snapshots['Snapshots']:
                print(f'snapshot, {snapshot["SnapshotId"]},{snapshot["StartTime"]}')

