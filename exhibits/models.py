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

