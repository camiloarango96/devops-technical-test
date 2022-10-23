from urllib import response
import boto3 

elb = boto3.client('elb', region_name='us-east-1')
r53 = boto3.client('route53')
lbs = elb.describe_load_balancers()
lb_DNS = (lbs['LoadBalancerDescriptions'][0]['DNSName'])

print(lb_DNS)

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

