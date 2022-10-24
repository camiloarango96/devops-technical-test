import boto3
import os 

rds = boto3.client('rds', 'us-east-1')

instances = rds.describe_db_instances()

host = instances['DBInstances'][0]['Endpoint']['Address']

name = instances['DBInstances'][0]['DBInstanceIdentifier']

print(name)

os.environ['DB_HOST'] = host
os.environ['DB_NAME'] = host
