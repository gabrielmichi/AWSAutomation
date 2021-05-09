##Script para criar uma máquina completa com tags - criado na aula de BOTO3 - Curso Cloud Ninja
def lambda_handler(event, context):
    
    #instancia
    ami="ami-0ac80df6eff0e70b5"
    type="t3.micro"
    
    #localizacao//network
    region="us-east-1"
    securitygroup=['sg-0470b15093ba11a69']
    subnet="subnet-0b1b8209393214a6d"
    
    #userdata
    user_data = '''#!/bin/bash
        sudo apt-get update
        sudo apt-get install -y nginx
        
        cd /var/www/html/
        git clone https://github.com/douglasmugnosit/cloudninja-demo-serverapp.git
        mv /var/www/html/cloudninja-demo-serverapp/* /var/www/html/
        rm -rf /var/www/html/cloudninja-demo-serverapp/'''
        
    #tags
    tags=[]
    tags.append({'Key': 'Name','Value': 'server'})
    tags.append({'Key': 'backup','Value': 'yes'})

    
    
    ec2_client = boto3.client('ec2', region_name=region)
    
    response = ec2_client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
        
                        'DeleteOnTermination': True,
                        'VolumeSize': 10,
                        'VolumeType': 'gp2'
                    },
                },
                {
                    'DeviceName': '/dev/xvdb',
                    'Ebs': {
        
                        'DeleteOnTermination': True,
                        'VolumeSize': 12,
                        'VolumeType': 'gp2'
                    },
                }
            ],
            SubnetId=subnet,
            ImageId=ami,
            InstanceType=type,
            UserData=user_data,
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': False
            },
            SecurityGroupIds=securitygroup,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': tags
                },
            ],
        )
        
        
    print(response)​