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

# env_file = os.getenv('GITHUB_ENV')
# with open(env_file, "a") as myfile:
#     myfile.write(db_host_string)
#     myfile.write(db_name_string)
    
cmd = 'kubectl set env deployment/flask-app DB_HOST=postgres DB_NAME={}'.format(host, name)

os.system('aws eks --region us-east-1 update-kubeconfig --name flask-clusterkubectl apply -f .')
os.system(cmd)