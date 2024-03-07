from django.urls import path

from .views import Home, upload_file, ProjectAutocomplete


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("upload/", upload_file, name='upload'),
    path("projects-autocomplete/", ProjectAutocomplete.as_view(), name='projects-autocomplete')
]