'''
En este script se obtiene el endpoint del balanceador de carga creado por k8s,
para luego crear un record en r53, esto con el objetivo de poder ingresar a la app
usando un dominio de r53 y su certificado

'''
import boto3 

elb = boto3.client('elb', region_name='us-east-1')
r53 = boto3.client('route53')
lbs = elb.describe_load_balancers()
lb_DNS = (lbs['LoadBalancerDescriptions'][0]['DNSName'])


paginator = r53.get_paginator('list_resource_record_sets')
flag = None

try:
    source_zone_records = paginator.paginate(HostedZoneId='Z0980157NFULAKVHAECQ')
    for record_set in source_zone_records:
        for record in record_set['ResourceRecordSets']:
            if record['Type'] == 'CNAME':
                flag = True

except Exception as error:
    print('An error occurred getting source zone records:')
    print(str(error))
    raise

if flag is None:

    response = r53.change_resource_record_sets(
        HostedZoneId = 'Z0980157NFULAKVHAECQ',
        ChangeBatch = {
            'Comment': 'Creo el record para el load balancer',
            "Changes": [{
                "Action": "CREATE",
                            "ResourceRecordSet": {
                                        "Name": "flask.olimac.link",
                                        "Type": "CNAME",
                                        "TTL": 300,
                                        "ResourceRecords": [{ "Value": lb_DNS}]
                        }}]
        }
    )
else:
    response = r53.change_resource_record_sets(
        HostedZoneId = 'Z0980157NFULAKVHAECQ',
        ChangeBatch = {
            'Comment': 'Creo el record para el load balancer',
            "Changes": [{
                "Action": "UPSERT",
                            "ResourceRecordSet": {
                                        "Name": "flask.olimac.link",
                                        "Type": "CNAME",
                                        "TTL": 300,
                                        "ResourceRecords": [{ "Value": lb_DNS}]
                        }}]
        }
    )

