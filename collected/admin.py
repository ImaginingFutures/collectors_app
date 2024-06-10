from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Article

# Register your models here.
admin.site.register(Article, ImportExportModelAdmin)