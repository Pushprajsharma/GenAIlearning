import requests
from transformers.utils import logging

logger = logging.get_logger(__name__)

class CustomHttpClient(requests.Session):
    def __init__(self):
        super().__init__()
        self.verify = False  # Disable SSL certificate verification
        self.headers.update({"User-Agent": "transformers/4.0.0"})
        logger.warning("SSL certificate verification is disabled.")

# Create a global instance of the custom HTTP client
custom_http_client = CustomHttpClient()
