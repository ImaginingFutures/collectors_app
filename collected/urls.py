from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleDetailHTMLView, ArticleCreateView, ArticleUpdateView

urlpatterns = [
    path('VolumeB/', ArticleListView.as_view(), name='article_list'),
    path('VolumeB/articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('VolumeB/articles/<int:pk>/html/', ArticleDetailHTMLView.as_view(), name='article_detail_html'),
]
