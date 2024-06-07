import requests
import base64
from django.conf import settings
import logging

# Configure logging for the application
logger = logging.getLogger("ifcollectors")

def generate_article_handle_url(article):
    handle_suffix = str(article.pk)
    handle = f"{settings.HANDLE_PREFIX}/{handle_suffix}"
    url = f"{settings.HANDLE_SYSTEM_URL}{handle}"
    data = {
        "values": [
            {
                "index": 1,
                "type": "URL",
                "data": {
                    "format": "string",
                    "value": f"https://create.ifrepo.world/article/{article.pk}"
                }
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {get_handle_auth()}'
    }
    try:
        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 201:
            return handle
        else:
            logger.error(f"Failed to register handle: {response.text}")
            return None  # Use None to indicate failure without raising an exception
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

def get_handle_auth():
    user_pass = f"{settings.HANDLE_USER}:{settings.HANDLE_PASSWORD}"
    encoded_u = base64.b64encode(user_pass.encode()).decode()
    return encoded_u
