import os
from dotenv import load_dotenv
load_dotenv()
import boto3
from botocore.exceptions import ClientError

region_name = os.getenv("region_name")
service_name = os.getenv('service_name')
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
bucketname = os.getenv('bucketname')

s3 = boto3.client(
service_name=service_name,
region_name=region_name,
aws_access_key_id=aws_access_key_id,
aws_secret_access_key=aws_secret_access_key
)


##############################################################################################
def getUrl(key, bucket_name):
    location = boto3.client('s3',region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key).get_bucket_location(Bucket=bucket_name)['LocationConstraint']

    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, key)
    return url
##############################################################################################
def upload_my_file(bucket, folder, file_to_upload, file_name):

    key = folder+"/"+file_name
    try:
        response = s3.upload_file(file_to_upload, bucket, key)
    except ClientError as e:
        print(e)
        return False , ""
    except FileNotFoundError as e:
        print(e)
        return False , ""
    return True , key
###############################################################################################
def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path
##########################################################################################################################################














