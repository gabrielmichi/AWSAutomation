##Script para alterar o tipo de instância EC2 - criado na aula de BOTO3 - Curso Cloud Ninja

def lambda_handler(event, context):
    client = boto3.client('ec2')
    
    # VARIAVEIS
    my_instance = 'i-0fa82869768ab03a7'
    new_type = 't2.large'
    
    # Stop Instancia
    print("Parando instancia")
    res = client.stop_instances(InstanceIds=[my_instance])
    print(res)
    
    # Aguarda instancia - wait
    print("Aguardando instancia ficar em stopped")
    waiter=client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[my_instance])
    
    #troca type
    res = client.modify_instance_attribute(
                                InstanceId=my_instance,
                                Attribute='instanceType', 
                                Value=new_type)
    print(res)
    
    # Inicia novamente
    print("Iniciando instancia")
    res = client.start_instances(InstanceIds=[my_instance])
    print(res)