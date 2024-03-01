from django.contrib import admin
from .models import UserProject, Contributor, NonUserProject
from CA_Django_connector.models import Place, Project
from filebox.models import UploadFile
from exhibits.models import Exhibit, MapExhibit

# Register your models here.
admin.site.register(Project)
admin.site.register(Place)
admin.site.register(UserProject)
admin.site.register(Contributor)
admin.site.register(NonUserProject)
admin.site.register(UploadFile)
admin.site.register(Exhibit)
admin.site.register(MapExhibit)
