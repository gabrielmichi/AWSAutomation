##​Script de criação de snapshots - criado na aula de BOTO3 - Curso Cloud Ninja
import boto3
import collections
import datetime
import time
import sys


def lambda_handler(event, context):
    today = datetime.datetime.today()
    today_timedate = today.strftime('%Y/%m/%d %H:%M:%S UTC')
    today_date = today.strftime('%Y/%m/%d') 
    retention_period = 15  # Delete snapshots after this many days
    deletion_counter = 0
    
    # Except after Monday (at Tuesday ~1am), since Friday is only 2 'working' days away:
    if datetime.date.today().weekday() == 1:
        retention_period = retention_period + 2


    deletion_date = today - datetime.timedelta(days=retention_period)
    deletion_date_string = deletion_date.strftime('%Y/%m/%d')
    
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions().get('Regions',[] )
    #all_regions = [region['RegionName'] for region in regions]
    all_regions = ['us-east-1','sa-east-1','us-west-2']
    
    
    #Log header
    print '+========================================================================================================+'
    print 'region_name:instance_name:instance_id:volume_id:snapshot_create_timedate:snapshot_id'
    
    
    for region_name in all_regions:
        ec2 = boto3.resource('ec2', region_name=region_name)


    # Now iterate through snapshots which were made by autsnap
        snapshots = ec2.snapshots.filter(
            Filters=[
                     {'Name': 'tag:MUGIT-auto_snap', 'Values': ['true']}
                    ]
                )
            
        for snapshot in snapshots:
            can_delete = False
            created_on_string=''
            create_timedate=''
            instance_name=''
            instance_id=''
            volume_id=''
            name=''
            
            for tag in snapshot.tags: 
                if tag['Key'] == 'created_date':
                    created_on_string = tag['Value']
                if tag['Key'] == 'create_timedate':
                    create_timedate = tag['Value']
                if tag['Key'] == 'instance_name':
                    instance_name = tag['Value']
                if tag['Key'] == 'instance_id':
                    instance_id = tag['Value']
                if tag['Key'] == 'volume_id':
                    volume_id = tag['Value']    
                if tag['Key'] == 'MUGIT-auto_snap':
                    if tag['Value'] == 'true':
                        can_delete = True
                if tag['Key'] == 'Name':
                    name = tag['Value']
                    
            created_on = datetime.datetime.strptime(created_on_string, '%Y/%m/%d').date()


            if created_on <= deletion_date.date() and can_delete == True:
                deletion_counter += 1
                snapshot_id = snapshot.id
                snapshot.delete()
                print '%s:%s:%s:%s:%s:%s' %(region_name,instance_name, instance_id, volume_id, create_timedate, snapshot_id )
    
    print "%s snapshots deleted." %(deletion_counter)
    print '+========================================================================================================+'