from django.contrib import admin
from .models import UserProject, Contributor, NonUserProject
from projects.models import Place, Project
from filebox.models import UploadFile

# Register your models here.
admin.site.register(Project)
admin.site.register(Place)
admin.site.register(UserProject)
admin.site.register(Contributor)
admin.site.register(NonUserProject)
admin.site.register(UploadFile)
