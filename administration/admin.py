from django.contrib import admin
from .models import Project, UserProject, Contributor, NonUserProject

# Register your models here.
admin.site.register(Project)
admin.site.register(UserProject)
admin.site.register(Contributor)
admin.site.register(NonUserProject)
