import os
from urllib.parse import urljoin

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class CustomStorage(S3Boto3Storage):
    """Custom storage for django_ckeditor_5 images on S3."""
    location = 'uploads/images'  # No media/ prefix - files are at bucket root
    file_overwrite = False
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
