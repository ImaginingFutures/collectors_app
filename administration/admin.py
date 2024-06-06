from django.contrib import admin
from .models import UserProject, Contributor, NonUserProject
from CA_Django_connector.models import (Place, Project, Themes, ExternalResource, ProjectTypes, ProjectParticipant, Keywords, Rights)
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from CA_Django_connector.models import UploadFile
from exhibits.models import Exhibit, MapExhibit, MapExhibitContribution

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('project_idno',)
        fields = ('project_idno', 'name', 'project_description', 'project_description_second', 
                  'type_of_project', 'themes', 'keywords', 'participants', 
                  'country_or_region', 'external_resources', 'thumbnail')
        exclude = ('id',)

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource

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
admin.site.register(Keywords, ImportExportModelAdmin)
admin.site.register(ExternalResource, ImportExportModelAdmin)
admin.site.register(ProjectTypes, ImportExportModelAdmin)
admin.site.register(ProjectParticipant, ImportExportModelAdmin)
admin.site.register(Rights, ImportExportModelAdmin)
