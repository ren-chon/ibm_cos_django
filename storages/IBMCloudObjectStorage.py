from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import ibm_boto3

class IBMCloudObjectStorage(S3Boto3Storage):

    def __init__(self, *args, **kwargs):
        self.bucket_name = getattr(settings, 'IBM_STORAGE_BUCKET_NAME', None)
        self.endpoint_url = getattr(settings, 'IBM_COS_ENDPOINT_URL', None)
        self.access_key = getattr(settings, 'IBM_COS_ACCESS_KEY_ID', None)
        self.secret_key = getattr(settings, 'IBM_COS_SECRET_ACCESS_KEY', None)
        self.service_instance_id = getattr(settings,
                                           'IBM_COS_SERVICE_INSTANCE_ID', None)
        self.ibm_api_key = getattr(settings, 'IBM_COS_API_KEY', None)
        self.ibm_auth_endpoint = getattr(
            settings, 'IBM_COS_AUTH_ENDPOINT',
            'https://iam.cloud.ibm.com/identity/token')

        self.ibm_cos_client = ibm_boto3.client(
            service_name='s3',
            ibm_api_key_id=self.ibm_api_key,
            ibm_service_instance_id=self.service_instance_id,
            ibm_auth_endpoint=self.ibm_auth_endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=ibm_boto3.session.Config(
                signature_version='oauth',
                s3={"payload_signing_enabled": True}),
            endpoint_url=self.endpoint_url)
        super().__init__(*args, **kwargs)

    def size(self, name):
        obj = self.ibm_cos_client.get_object(Bucket=self.bucket_name, Key=name)
        return obj['ContentLength']

    def exists(self, name):
        try:
            self.ibm_cos_client.head_object(Bucket=self.bucket_name, Key=name)
            return True
        except:
            return False

    def _save(self, name, content):
        self.ibm_cos_client.upload_fileobj(content.file,
                                           Bucket=self.bucket_name,
                                           Key=name)
        return name

    def delete(self, name):
        self.ibm_cos_client.delete_object(Bucket=self.bucket_name, Key=name)

    def _open(self, name, mode='rb'):
        obj = self.ibm_cos_client.get_object(Bucket=self.bucket_name, Key=name)
        return obj['Body']

    # -----------------#
    #   Not Working    #
    # -----------------#
    
    # def url(self, name):
    #     url = self.ibm_cos_client.generate_presigned_url(ClientMethod='get_object',
    #                                                  Params={
    #                                                      'Bucket':
    #                                                      self.bucket_name,
    #                                                      'Key': name
    #                                                  },
    #                                                  HttpMethod='GET',
    #                                                  ExpiresIn=3600)
    #     return url
