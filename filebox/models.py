from django.db import models
from projects.models import Project, Place

    
class UploadFile(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    