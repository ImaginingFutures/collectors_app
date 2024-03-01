from django.db import models
from polymorphic.models import PolymorphicModel
# Create your models here.


class Exhibit(PolymorphicModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey('CA_Django_connector.Project', on_delete=models.CASCADE, related_name='exhibits')

    def __str__(self):
        return self.title
    
class MapExhibit(Exhibit):
    map_data = models.JSONField(help_text="Data specific to rendering maps")

""" class GalleryExhibit(Exhibit):
    images = models.ManyToManyField('YourImageModel', related_name='galleries') """


class Contributions(models.Model):
    pass

class MapExhibitContribution(models.Model):
    
    name = models.CharField(max_length=150, blank=True, null=True)
    recipe_name = models.CharField(max_length=150)
    recipe = models.TextField(max_length=2000, help_text="2000 characters max")
    cultural_connections = models.TextField(max_length=1000, help_text="Add your personal/cultural connection with that recipe")
    media = models.FileField(upload_to='uploads/', help_text='Share files under 100MB')
