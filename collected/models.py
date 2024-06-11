from django.db import models
from CA_Django_connector.models import ProjectParticipant, Project, Keywords, Rights
from PIL import Image
from io import BytesIO
import re
from django.core.files import File
from django_ckeditor_5.fields import CKEditor5Field
from pdf2image import convert_from_bytes
from bs4 import BeautifulSoup

import logging

logger = logging.getLogger("ifcollectors")

class Article(models.Model):
    authors = models.ManyToManyField(ProjectParticipant)
    projects = models.ManyToManyField(Project)
    keywords = models.ManyToManyField(Keywords, blank=True)
    title = models.CharField(max_length=200)
    abstract = CKEditor5Field(max_length=5000, null=True, blank=True, config_name="extends")
    rights = models.ForeignKey(Rights, on_delete=models.CASCADE)
    filePDF = models.FileField(upload_to='pdfs/')
    contentHTML = CKEditor5Field(null=True, blank=True, config_name="extends")
    handle_url = models.URLField(max_length=200, blank=True, null=True) # null and blank to allow article creation before a handle url have been assigned to that url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.FileField(upload_to='thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Creating a thumbnail
        if self.filePDF and not self.thumbnail:
            images = convert_from_bytes(self.filePDF.read())
            
            if images:
                
                first_page = images[0]
                first_page.thumbnail((300, 300))
                
                temp_thumb = BytesIO()
                first_page.save(temp_thumb, format="JPEG")
                temp_thumb.seek(0)
                
                self.thumbnail.save(self.filePDF.name.split('.')[0] + '_thumb.jpg', File(temp_thumb), save=False)
        
        ## support anchor links because CKEditor 5 hasn't implemented that feature yet :\ 
        ## https://github.com/ckeditor/ckeditor5/issues/1944
        soup = BeautifulSoup(self.contentHTML, 'html.parser')
        
        for index, anchor in enumerate(soup.find_all('a', href=True), start=1):
            if not anchor.get('id'):
                # get the href url
                href = anchor.get('href')
                try:
                    id = re.findall(r'\d+', href)
                    if href.startswith("#_ednr"):
                        anchor['id'] = f'_edn{id[0]}'
                    else:
                        anchor['id'] = f'_ednref{id[0]}'
                except IndexError:
                    logger.warning(f"Skipping url from anchor: {href}")
        
        self.contentHTML = str(soup)
        
        super(Article, self).save(*args, **kwargs)
        
    def __str__(self):
        authors = ", ".join([author.full_name for author in self.authors.all()])
        return f"{authors}, \"{self.title}\""
            