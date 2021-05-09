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
    snapshot_counter_total = 0
    
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions().get('Regions',[] )
    #all_regions = [region['RegionName'] for region in regions]
    all_regions = ['us-east-1','sa-east-1','us-west-2']
    
    
    #Log header
    print '+=========================================================================================+'
    print 'region:instance_name:instance_id:instance_state:volumes:snapshot_counter:snap_size_counter'
    
    for region_name in all_regions:
        ec2 = boto3.resource('ec2', region_name=region_name)


        #We only want to look through instances with the following tag key value pair: MUGIT-auto_snapshot : true
        instances = ec2.instances.filter(
            Filters=[{'Name': 'tag:MUGIT-auto_snapshot', 'Values': ['true']}]
                )
                
        for instance in instances.all():
            instance_name = ''
            device_mapper = ''
            snapshot_counter = 0
            snap_size_counter = 0
            volume_ids = []
            for tag in instance.tags: 
              if tag['Key'] == 'Name':
                  instance_name = tag['Value']
                  
            volumes = instance.volumes.all() 
            for volume in volumes:
                volume_ids.append(volume.id)
                
                #Check device mapper
                device_mapper = ec2.Volume(volume.id).attachments[0]['Device']


                snapshot = volume.create_snapshot(
                    Description = '[MUGIT] - AutoSnapshot of %s, on volume %s - Created %s' %(instance_name, volume.id, str(today_timedate)),
                    )
                    
                snapshot.create_tags( 
                    Tags = [
                        {
                        'Key': 'MUGIT-auto_snap',
                        'Value': 'true'
                        },
                        {
                        'Key': 'volume_id',
                        'Value': volume.id
                        },
                        {
                        'Key': 'create_timedate',
                        'Value': today_timedate
                        },
                        {
                        'Key': 'Name',
                        'Value': '%s - autosnap' %(instance_name)
                        },
                        {
                        'Key': 'device_mapper',
                        'Value': '%s' %(device_mapper)
                        },
                        {
                        'Key': 'instance_name',
                        'Value': '%s' %(instance_name)
                        },
                        {
                        'Key': 'instance_id',
                        'Value': '%s' %(instance.id)
                        },
                        {
                        'Key': 'instance_state_during_snapshot',
                        'Value': '%s' %(instance.state['Name'])
                        },
                        {
                        'Key': 'created_date',
                        'Value': today_date
                        }
                    ]
                )
                snapshot_counter += 1
                snapshot_counter_total += 1
                snap_size_counter += snapshot.volume_size
                    
            print '%s:%s:%s:%s:%s:%s:%s' %(region_name,instance_name, instance.id, instance.state['Name'], volume_ids,str(snapshot_counter),str(snap_size_counter))
            
    print "%s snapshots created." %(snapshot_counter_total)
    print '+========================================================================================================+'