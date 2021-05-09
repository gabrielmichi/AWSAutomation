import boto3
import sys, traceback
from datetime import datetime
from time import sleep
import pytz

#########
#1 . Só funciona pra servidores com a tag awscloudninja-schedule-stop-start == True
#2 . awscloudninja-schedule-stop  = tag com horário para parar a instância
#3 . awscloudninja-schedule-start = tag com horário para iniciar a instância
#4 . awscloudninja-schedule-dow   = dias da semana que são validos para automação (0=domingo, 1=Segunda...6=sabado)
####

def start_ec2_instances(totalMinutesNow,todayDayOfWeek):
    start_time = datetime.now()

    # starting ec2 client
    ec2_client = boto3.client('ec2')

    regions = ec2_client.describe_regions()

    for region in regions['Regions']:
        try:
            print("Region: " + str(region['RegionName']))
            ec2_client = boto3.client('ec2', region_name=region['RegionName'])
            instances = ec2_client.describe_instances()
            instanceIds = list()
            
            #PERCORRE POR TODOS SERVERS
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    #FILTRA APENAS POR SERVIDORES COM STATUS STOPPED
                    if instance['State']['Name'] == "stopped" and not instance['Tags'] is None : 
                        
                        #CONVERTO FORMATO DE TAG PARA DICIONARIO
                        tagDict={}
                        for tag in instance['Tags']:
                            tagDict[tag['Key']] = tag['Value'] 
                            if 'awscloudninja-schedule-stop-start' not in tagDict:
                                tagDict['awscloudninja-schedule-stop-start'] = 'False'
                        
                        #VERIFICA QUAIS INSTACIAS ESTAO COM AUTOMACAO ATIVA
                        if tagDict['awscloudninja-schedule-stop-start'] == 'True':
                            #Pega valor da tag start
                            try:
                                startInstace=0
                                #VERIFICA DIA DA SEMANA
                                if 'awscloudninja-schedule-dow' in tagDict:
                                    if todayDayOfWeek in list(tagDict['awscloudninja-schedule-dow'].split(',')):
                                        startInstace=startInstace+1
                                        
                                #VERIFICA SE O HORÁRIO ESTA CERTO
                                #AO INVES DE TRABALHAR COM DATETIME E DATEDELTA
                                #EU CONVERTO PRA MINUTOS PRA FICAR MAIS FACIL
                                if 'awscloudninja-schedule-start' in tagDict:
                                    startTotalMinute=int(tagDict['awscloudninja-schedule-start'].split(':')[0])*60+int(tagDict['awscloudninja-schedule-start'].split(':')[1])
                                    if (totalMinutesNow >= startTotalMinute):
                                        startInstace=startInstace+1
                                        
                                #ADICIONA NA LISTA DE START
                                if startInstace == 2:
                                    instanceIds.append(instance['InstanceId'])
                            
                            except:
                                print("Not expected error:", traceback.print_exc())
                                continue
                            
            if len(instanceIds) > 0 : 
                print ("Iniciando instancias: " + str(instanceIds))
                ec2_client.start_instances(InstanceIds=instanceIds)                                                   
                                                            
        except:
            print("Not expected error:", traceback.print_exc())
                                                           
    end_time = datetime.now()
    took_time = end_time - start_time
    print ("Total time of execution: " + str(took_time) )  

def stop_ec2_instances(totalMinutesNow,todayDayOfWeek):
    start_time = datetime.now()

    # starting ec2 client
    ec2_client = boto3.client('ec2')

    regions = ec2_client.describe_regions()

    for region in regions['Regions']:
        try:
            print("Region: " + str(region['RegionName']))
            ec2_client = boto3.client('ec2', region_name=region['RegionName'])
            instances = ec2_client.describe_instances()
            instanceIds = list()
            
            #PERCORRE POR TODOS SERVERS
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    #FILTRA APENAS POR SERVIDORES COM STATUS RUNNING
                    if instance['State']['Name'] == "running" and not instance['Tags'] is None : 
                        
                        #CONVERTO FORMATO DE TAG PARA DICIONARIO
                        tagDict={}
                        for tag in instance['Tags']:
                            tagDict[tag['Key']] = tag['Value'] 
                            if 'awscloudninja-schedule-stop-start' not in tagDict:
                                tagDict['awscloudninja-schedule-stop-start'] = 'False'
                        
                        #VERIFICA QUAIS INSTACIAS ESTAO COM AUTOMACAO ATIVA
                        if tagDict['awscloudninja-schedule-stop-start'] == 'True':
                            
                            try:
                                stopInstance=0
                                
                                #VERIFICA DIA DA SEMANA
                                if 'awscloudninja-schedule-dow' in tagDict:
                                    if todayDayOfWeek in list(tagDict['awscloudninja-schedule-dow'].split(',')):
                                        stopInstance=stopInstance+1
                                
                                #VERIFICA SE O HORÁRIO ESTA CERTO
                                #AO INVES DE TRABALHAR COM DATETIME E DATEDELTA
                                #EU CONVERTO PRA MINUTOS PRA FICAR MAIS FACIL
                                if 'awscloudninja-schedule-stop' in tagDict:
                                    startTotalMinute=int(tagDict['awscloudninja-schedule-stop'].split(':')[0])*60+int(tagDict['awscloudninja-schedule-stop'].split(':')[1])
                                    if (totalMinutesNow >= startTotalMinute):
                                        stopInstance=stopInstance+1
                                        
                                #ADICIONA NA LISTA DE START
                                if stopInstance == 2:
                                    instanceIds.append(instance['InstanceId'])
                                
                            except:
                                print("Not expected error:", traceback.print_exc())
                                continue
                            
            if len(instanceIds) > 0 : 
                print ("Parando instancias: " + str(instanceIds))
                ec2_client.stop_instances(InstanceIds=instanceIds, Force=False)                                                  
                                                            
        except:
            print("Not expected error:", traceback.print_exc())
                                                           
    end_time = datetime.now()
    took_time = end_time - start_time
    print ("Total time of execution: " + str(took_time) )  

def get_current_date_in_minutes():
    tz = pytz.timezone('America/Sao_Paulo')
    utc_time=datetime.utcnow()
    utc_time=utc_time.replace(tzinfo=pytz.UTC)
    now=utc_time.astimezone(tz)
    totalMinutesNow=int(now.strftime("%H"))*60+int(now.strftime("%M"))
    return totalMinutesNow
    
def lambda_handler(event, context):
    
    #DECLARA VARIAVEIS
    totalMinutesNow = get_current_date_in_minutes()
    todayDayOfWeek  = datetime.today().strftime('%w')
    print(todayDayOfWeek)
    
    print('Iniciando instancias... ')
    start_ec2_instances(totalMinutesNow,todayDayOfWeek)
    
    print('Parando instancias... ')
    stop_ec2_instances(totalMinutesNow,todayDayOfWeek)
