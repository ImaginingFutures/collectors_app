from django.test import TestCase
from .models import Article
from utils.handle_utils import generate_article_handle_url

class HandleURLTestCase(TestCase):
    def test_generate_handle_url(self):
        # Create a test article instance
        article = Article(title="Test", abstract="Test abstract")
        article.pk = 1  # Set a known primary key

        # Test handle generation
        handle_url = generate_article_handle_url(article)
        expected_url = f"http://165.22.119.86:8000/api/handles/20.500.14542/1"
        self.assertIsNotNone(handle_url)
        self.assertEqual(handle_url, expected_url)
