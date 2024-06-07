from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'abstract', 'authors', 'projects', 'keywords', 'filePDF', 'thumbnail', 'rights']
