from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Place(models.Model):
    
    place_name = models.CharField(max_length=100)
    place_type = models.CharField(max_length=50, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    is_part_of = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    def __str__(self) -> str:
        return f'{self.place_name} ({self.place_type})'


class Languages(models.Model):
    
    language = models.CharField(max_length=100)
    iso_language_name = models.CharField(max_length=100)
    alpha2 = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)

    history = HistoricalRecords()
    
class Themes(models.Model):
    
    theme = models.CharField(max_length=70, unique=True, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.theme = self.theme.lower() if self.theme else ''
        if Themes.objects.filter(theme=self.theme).exists():
            raise ValidationError(f"This term '{self.theme}' already exists.")
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.theme}"

class Keywords(models.Model):
    
    keyword = models.CharField(max_length=70, unique=True, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.keyword = self.keyword.lower() if self.keyword else ''
        if Keywords.objects.filter(keyword=self.keyword).exists():
            raise ValidationError(f"This term '{self.keyword}' already exists.")
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.keyword}"

class Rights(models.Model):
    
    license = models.CharField(max_length=100)
    license_abreviation = models.CharField(max_length=20)
    license_expanded = models.CharField(max_length = 600)
    canonical_url = models.URLField(unique=True, null=True)
    icon_url = models.URLField(unique=True, null=True)
    
    def __str__(self) -> str:
        return f"({self.license_abreviation}) {self.license}"

class ExternalResource(models.Model):
    
    type_of_resource = models.CharField(max_length=80,
        choices=(
            ('web', 'Website'),
            ('exh', 'Exhibit'),
            ('pub', 'Publication')
        ), default='web'
    )
    resource_name = models.CharField(max_length=200, unique=True)
    url = models.URLField(unique=True)
    
    def __str__(self) -> str:
        return f"{self.resource_name}"
    
class ProjectTypes(models.Model):
    
    project_type = models.CharField(max_length=200, unique=True)
    type_description = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.project_type}'

class SecondLangDescriptions(models.Model):
    
    project_description = models.TextField(max_length=1000)
    language = models.CharField(max_length=20, null=True, blank=True)

class ProjectParticipant(models.Model):
    
    full_name = models.CharField(max_length=300)
    email = models.EmailField(blank=True, null=True)
    project_role = models.CharField(max_length=200, blank=True)
    
    
    def __str__(self) -> str:
        return f'{self.full_name}'

class Project(models.Model):
    """
    Reduced model for the table ca_collections
    """
    
    project_idno = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, unique=True,)
    project_description = CKEditor5Field(max_length=10000, null=True, blank=True, config_name="extends")
    project_description_second = CKEditor5Field(max_length=10000, null=True, blank=True, config_name="extends")
    
    type_of_project = models.ForeignKey(ProjectTypes, on_delete=models.CASCADE)
    
    themes = models.ManyToManyField(Themes, blank=True)
    keywords = models.ManyToManyField(Keywords, blank=True)
    
    users = models.ManyToManyField(User, through='administration.UserProject', blank=True)
    participants = models.ManyToManyField(ProjectParticipant, blank=True, related_name="project_participants")
    country_or_region = models.ManyToManyField(Place, blank=True)
    external_resources = models.ManyToManyField(ExternalResource, blank=True)
    
    thumbnail = models.ImageField(upload_to='thumbnails/', help_text='Share files under 10MB', blank=True, null=True)  
    thumbnail_rights = models.ForeignKey(Rights, on_delete=models.DO_NOTHING, related_name="thumbnail_rights", null=True)
    thumbnail_note = models.CharField(max_length=250, blank=True, null=True)
    
    history = HistoricalRecords()
    
    class Meta:
        permissions = [
            ("edit_project", "Can edit project"),
        ]
    
    def __str__(self) -> str:
        return f'{self.name}'

class UploadFile(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')

class Records(models.Model):
    """
    Reduced model for ca_objects
    """
    
    record_idno = models.CharField(max_length=100, unique=True)
    collection = models.ManyToManyField(Project)
    preferred_labels = models.CharField(max_length=200)
    langmaterial = models.ManyToManyField(Languages, blank=True)
    themes = models.ManyToManyField(Themes, blank=True)
    places = models.ManyToManyField(Place, blank=True)
    date_creation = models.DateField(blank=True, null=True)
    creator = models.ManyToManyField(User, blank=True, related_name='creators')
    rights_holders = models.ManyToManyField(User, blank=True, related_name='rights_holders')
    license = models.ForeignKey(Rights, on_delete=models.SET_DEFAULT, default=1)
    media = models.ManyToManyField(UploadFile, blank=True)
    
    history = HistoricalRecords()


    