import ConfigParser
import boto
import io
from boto.s3.key import Key

AWS_ACCESS_KEY = os.environ.get('S3-ACCESSKEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('S3-SECRETKEY')
S3_BUCKET = os.environ.get('S3-BUCKET')

def s3_upload(uploaded_file, username):
    ## Sets up access variables for the S3 bucket
    s3conn = boto.connect_s3(AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY)
    bucket = s3conn.get_bucket(S3_BUCKET)

    # k is the file and key is the filename, i think ??
    k = Key(bucket)
    print username
    k.key = str(username)
    k.content_type = uploaded_file.content_type
    print str(k)

    if hasattr(uploaded_file,'temporary_file_path'):
        k.set_contents_from_filename(uploaded_file.temporary_file_path())
    else:
        k.set_contents_from_string(uploaded_file.read())

    k.set_canned_acl('public-read')

    return k.generate_url(expires_in=0, query_auth=False)