# IBM Cloud Object Storage with Django

This package extends the S3Boto3Storage class from Django Storages to provide a storage backend for IBM Cloud Object Storage (COS). It uses the ibm_boto3 library to interact with the COS API.

## Dependencies
Install these packages via pip:

```bash
pip install django-storages ibm-cos-sdk
```
## Configuration

To use the IBMCloudObjectStorage class in your Django project, follow these steps:

Copy the `IBMCloudObjectStorage.py` file to a location in your Django project, such as a storage directory.

In your Django settings.py file, add the following settings:

```python
# settings.py

DEFAULT_FILE_STORAGE = 'path.to.IBMCloudObjectStorage'
IBM_STORAGE_BUCKET_NAME = 'my_bucket_name'
IBM_COS_ENDPOINT_URL = 'https://s3.us.cloud-object-storage.appdomain.cloud'
IBM_COS_ACCESS_KEY_ID = 'my_access_key_id'
IBM_COS_SECRET_ACCESS_KEY = 'my_secret_access_key'
IBM_COS_SERVICE_INSTANCE_ID = 'my_service_instance_id'
IBM_COS_API_KEY = 'my_api_key'
```
You can find the values for `IBM_COS_ENDPOINT_URL`, `IBM_COS_ACCESS_KEY_ID`, `IBM_COS_SECRET_ACCESS_KEY`, `IBM_COS_SERVICE_INSTANCE_ID`, and `IBM_COS_API_KEY` in your IBM Cloud Object Storage service credentials.

## Usage
Once you have set up the configuration parameters, you can use the IBM Cloud Object Storage backend in your Django project:

```python
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Save a file
default_storage.save('my_file.txt', ContentFile('hello'))

# Get the URL of a file
url = default_storage.url('my_file.txt')

# Check if a file exists
exists = default_storage.exists('my_file.txt')

# Delete a file
default_storage.delete('my_file.txt')
```
## Limitation
The `url()` method for generating a presigned URL is not working in this implementation. If you need to generate a presigned URL, you can use the `generate_presigned_url()` method from the ibm_boto3 client directly.