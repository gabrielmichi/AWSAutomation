import json
import boto3

##criado na aula de BOTO3 - Curso Cloud Ninja
##Sempre consultar se o servico utilizar paginacao atraves do NextToken
##AWS pode devolver o valor "picado" nessário realizar paginacao
def lambda_handler(event, context):
    
    region="us-east-1"
    
    
    #0 - faz conexao
    ec2_client = boto3.client('ec2', region_name=region)
    
    #1 - Pega 5 instancias / paginacao
    instances = ec2_client.describe_instances(MaxResults=5)  
   
    #2 - Pecorre a lista
    if instances['Reservations']:
        
        while True:
            print(" entrei na paginacao ")
            
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    print(instance['InstanceId'])
                   
            if 'NextToken' not in instances: break
            next_token =   instances['NextToken']
            instances    =   ec2_client.describe_instances(MaxResults=5,NextToken=next_token)​