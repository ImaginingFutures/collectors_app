from django.contrib import admin
from .models import UserProject, Contributor, NonUserProject
from CA_Django_connector.models import Place, Project, Themes, ExternalResource

from import_export.admin import ImportExportModelAdmin

from filebox.models import UploadFile
from exhibits.models import Exhibit, MapExhibit, MapExhibitContribution


# Register your models here.
admin.site.register(Project, ImportExportModelAdmin)
admin.site.register(Place, ImportExportModelAdmin)
admin.site.register(UserProject, ImportExportModelAdmin)
admin.site.register(Contributor, ImportExportModelAdmin)
admin.site.register(NonUserProject, ImportExportModelAdmin)
admin.site.register(UploadFile, ImportExportModelAdmin)
admin.site.register(Exhibit, ImportExportModelAdmin)
admin.site.register(MapExhibit, ImportExportModelAdmin)
admin.site.register(MapExhibitContribution, ImportExportModelAdmin)
admin.site.register(Themes, ImportExportModelAdmin)
admin.site.register(ExternalResource, ImportExportModelAdmin)
