from django.urls import path

from .views import home, upload_file, ProjectAutocomplete


urlpatterns = [
    path("", home, name="home"),
    path("upload/", upload_file, name='upload'),
    path("projects-autocomplete/", ProjectAutocomplete.as_view(), name='projects-autocomplete')
]