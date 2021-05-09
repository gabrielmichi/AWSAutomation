##Script checa tags do servidor, e cria caso não exista - criado na aula de BOTO3 - Curso Cloud Ninja
import boto3

def lambda_handler(event, context):
    
    region="us-east-1"
    instancia="i-01ddfd68babb23d82"
    tags={}
    
    
    #0 - faz conexao
    ec2_client = boto3.client('ec2', region_name=region)
    
    #1. Pega todas tags do servidor
    response = ec2_client.describe_instances(InstanceIds=[instancia])
    for instance_tag in response['Reservations'][0]['Instances'][0]['Tags']:
        tags[instance_tag['Key']]   = instance_tag['Value']
    
    #2 - checa tags atuais e cria se não existir
    if 'Name' not in tags:
        tags['Name']   = "notdefined"
    if 'App' not in tags:
        tags['App']   = "notdefined"
    if 'env' not in tags:
        tags['env']   = "notdefined"
    if 'owner' not in tags:
        tags['owner']   = "notdefined"
    if 'centro-de-custo' not in tags:
        tags['centro-de-custo']   = "notdefined"
    
    #3 - converte pro formato necessario
    newTags=[]
    for tag in tags:
        newTags.append({'Key':tag, 'Value':tags[tag]})
    print(newTags)
        
    res = ec2_client.create_tags(Resources=[instancia], Tags=newTags)
    print(res)​