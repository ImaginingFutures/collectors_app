from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# Create your models here.

class Place(models.Model):
    
    place_name = models.CharField(max_length=100)
    place_type = models.CharField(max_length=50, null=True)
    geolocation = models.CharField(max_length=100, blank=True, null=True)
    
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
    
    theme = models.CharField(max_length=70)
    history = HistoricalRecords()

class Rights(models.Model):
    
    license = models.CharField(max_length=100)
    license_abreviation = models.CharField(max_length=20)
    license_expanded = models.CharField(max_length = 200)
    
    history = HistoricalRecords()

class Project(models.Model):
    """
    Reduced model for the table ca_collections
    """
    project_idno = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, unique=True,)
    project_description = models.TextField(max_length=1000, null=True)
    country_or_region = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    type_of_project = models.CharField(max_length=80, choices=(('startup', 'Start Up Projects (2020-21)'), 
                                               ('followon', 'Follow On Grants (2021-22)'),
                                               ('phase1', 'Phase 1 projects - commissions (2021-22)'),
                                               ('phase2', 'Phase 2 projects - commissions (2021-22)'),
                                               ('africa', 'Africa'),
                                               ('asiapac', 'Asia Pacific'),
                                               ('europemeast', 'Europe & Middle East'),
                                               ('vvlocs', 'Various Locations'),
                                               ('further', 'Further initiatives'),
                                               ('maprojects', 'MA Projects')), default='startup')
    
    
    users = models.ManyToManyField(User, through='administration.UserProject')
    
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return f'{self.name}'

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
    media = models.ManyToManyField('filebox.UploadFile', blank=True)
    
    history = HistoricalRecords()
