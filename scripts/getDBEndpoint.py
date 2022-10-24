import boto3
import os 

rds = boto3.client('rds', 'us-east-1')

instances = rds.describe_db_instances()

host = instances['DBInstances'][0]['Endpoint']['Address']

name = instances['DBInstances'][0]['DBInstanceIdentifier']

db_host_string = "DB_HOST={}\n".format(host)
db_name_string = "DB_NAME={}".format(name)

print(db_host_string)
print(db_name_string)

env_file = os.system('GITHUB_ENV')
with open(env_file, "w") as myfile:
    myfile.write(db_host_string)
    myfile.write(db_name_string)