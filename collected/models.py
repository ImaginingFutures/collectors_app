from django.db import models
from CA_Django_connector.models import ProjectParticipant, Project, Keywords, Rights
from utils.handle_utils import generate_article_handle_url

class Article(models.Model):
    authors = models.ManyToManyField(ProjectParticipant)
    projects = models.ManyToManyField(Project)
    keywords = models.ManyToManyField(Keywords)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    rights = models.ForeignKey(Rights, on_delete=models.CASCADE)
    filePDF = models.FileField(upload_to='pdfs/')
    handle_url = models.CharField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.FileField(upload_to='thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.handle_url:
            # Assume you have a function to generate a handle URL here
            self.handle_url = generate_article_handle_url(self)
        super().save(*args, **kwargs)
