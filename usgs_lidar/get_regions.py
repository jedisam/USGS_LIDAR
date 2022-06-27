"""Get regions from s3 bucket."""
import boto3
from botocore import UNSIGNED
from botocore.config import Config

# s3 = boto3.resource("s3")
s3 = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
# s3 = boto3.resource("s3", use_ssl=False, verify=False)

my_bucket = s3.Bucket("usgs-lidar-public")
regions_list = []
for object_summary in my_bucket.objects.filter(Prefix=""):
    if object_summary.key.split("/")[0] not in regions_list:
        regions_list.append(object_summary.key.split("/")[0])
    # print(object_summary.key)

print(len(regions_list))

# aws s3 ls s3://usgs-lidar-public/ --no-sign-reques

