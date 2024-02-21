from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, through='administration.UserProject')
    
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return f'{self.name}'