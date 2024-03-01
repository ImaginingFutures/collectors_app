from django.db import models
    
class UploadFile(models.Model):
    project = models.ForeignKey('CA_Django_connector.Project', related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    