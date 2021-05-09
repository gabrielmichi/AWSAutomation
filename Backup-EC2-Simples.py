##Backup Simples de instâncias EC2 - criado na aula de BOTO3 - Curso Cloud Ninja

import json
import boto3

def lambda_handler(event, context):
    
    #VARIAVEIS
    instancia="i-0fa82869768ab03a7"
    backup_name="Nome-do-backup"
    backup_description="imagem de bla bla bla"
    reboot=False
    
    client = boto3.client('ec2')
    
    response = client.create_image(
        Description=backup_description,
        InstanceId=instancia,
        Name=backup_name,
        NoReboot=reboot
    )
    
    print(response)