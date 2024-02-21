from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from projects.models import Project

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
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'User Project'
        verbose_name_plural = 'User Projects'
        unique_together = (('user', 'project'),)
    
    def __str__(self) -> str:
        return f'{self.user} < > {self.project}'


class NonUserProject(models.Model):
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'User non registered Project'
        verbose_name_plural = 'User non registered Projects'
        unique_together = (('user', 'project'),)
    
    def __str__(self) -> str:
        return f'{self.user} < > {self.project}'