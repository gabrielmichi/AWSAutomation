##Script de Start/stop com condição de WAIT - criado na aula de BOTO3 - Curso Cloud Ninja

import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('ec2')
    
    # VARIAVEIS
    my_instance = 'i-0fa82869768ab03a7'
    
    # Stop Instancia
    print("Parando instancia")
    res = client.stop_instances(InstanceIds=[my_instance])
    print(res)
    
    # Aguarda instancia - wait
    print("Aguardando instancia ficar em stopped")
    waiter=client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[my_instance])
    
    
    # Inicia novamente
    print("Iniciando instancia")
    res = client.start_instances(InstanceIds=[my_instance])
    print(res)