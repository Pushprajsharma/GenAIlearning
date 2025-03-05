import ssl
import requests

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Optionally, you can also disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
