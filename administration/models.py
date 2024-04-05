from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from simple_history.models import HistoricalRecords
from CA_Django_connector.models import Project

class Contributor(models.Model):
    """
    Model to be used with external persons that doesn't have to be registered
    in the platform
    """
    name = models.CharField(max_length=100)
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return f'{self.name}'
    

class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    
    is_lead = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'User Project'
        verbose_name_plural = 'User Projects'
        unique_together = (('user', 'project'),)
    
    def __str__(self) -> str:
        return f'{self.user} < > {self.project}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(Project)
        perm = Permission.objects.get(codename='edit_project', content_type=content_type)
        if self.is_lead:
            self.user.user_permissions.add(perm)
        else:
            self.user.user_permissions.remove(perm)


class NonUserProject(models.Model):
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_lead = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'User non registered Project'
        verbose_name_plural = 'User non registered Projects'
        unique_together = (('user', 'project'),)
    
    def __str__(self) -> str:
        return f'{self.user} < > {self.project}'