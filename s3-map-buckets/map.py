#!/usr/local/bin/python3

import pprint
import boto3
import mdutils
import json

# setup some generic stuff, boto object, pprint
s3 = boto3.client('s3', region_name="us-west-1")
response = s3.list_buckets()
pp = pprint.PrettyPrinter(indent=4)


# lets frame up the markdown document

mdDoc = mdutils.MdUtils(file_name='s3-bucket-inventory', title='S3 Bucket Inventory')


#print('\n*** mapping buckets ***\n')
for bucket in response['Buckets']:
    n = bucket["Name"]
    #print("\n# %s \n" % n)
    mdDoc.new_header(level=1,title=str(n))

    # first lets check bucket policy
    mdDoc.new_header(level=2,title="Bucket Policy")
    try:
        bucket_policy = s3.get_bucket_policy(Bucket=n)
        statement = json.loads(bucket_policy["Policy"])
        temp = str(statement["Statement"])
        end = len(temp)-1
        r = temp[1:end]
        mdDoc.insert_code(json.dumps(r, indent=2, sort_keys=True))
    except Exception as e:
        #print(e)
        mdDoc.new_paragraph("No policy detected for this bucket")

    # bucket versioning
    mdDoc.new_header(level=2,title="Bucket Versioning")
    try:
        bucket_version = s3.get_bucket_versioning(Bucket=n)
        mdDoc.new_paragraph(json.dumps(bucket_version["Status"], indent=2, sort_keys=True))
    except Exception as e:
        mdDoc.new_paragraph("No Versioning configured for this bucket")

    # bucket tagging
    mdDoc.new_header(level=2,title="Bucket Tagging")
    try:
        bucket_tagging = s3.get_bucket_tagging(Bucket=n)
        mdDoc.insert_code(json.dumps(bucket_tagging["TagSet"], indent=2, sort_keys=True))
    except Exception as e:
        #print(e)
        mdDoc.new_paragraph("No Tagging information found for this bucket")

    # bucket acl
    mdDoc.new_header(level=2,title="Bucket ACL")
    try:
        bucket_acl = s3.get_bucket_acl(Bucket=n)

        mdDoc.new_header(level=3, title="Owner")
        mdDoc.insert_code(json.dumps(bucket_acl["Owner"], indent=2, sort_keys=True)) 
        mdDoc.new_header(level=3, title="Grants")
        mdDoc.insert_code(json.dumps(bucket_acl["Grants"], indent=2, sort_keys=True)) 
    except Exception as e:
        #print(e)
        mdDoc.new_paragraph("No ACL found for this bucket")
    
    # bucket logging
    mdDoc.new_header(level=2,title="Bucket Logging")
    try:
        bucket_logging = s3.get_bucket_logging(Bucket=n)
        mdDoc.insert_code(json.dumps(bucket_logging["LoggingEnabled"], indent=2, sort_keys=True))
    except Exception as e:
        #print(e)
        mdDoc.new_paragraph("No Logging found for this bucket")

    # bucket encryption
    mdDoc.new_header(level=2,title="Bucket Encryption")
    try:
        bucket_encryption = s3.get_bucket_encryption(Bucket=n)
        mdDoc.insert_code(json.dumps(bucket_encryption["ServerSideEncryptionConfiguration"], indent=2, sort_keys=True))
    except Exception as e:
        #print(e)
        mdDoc.new_paragraph("No Encryption found for this bucket")
    
    mdDoc.new_paragraph("---")
mdDoc.create_md_file()