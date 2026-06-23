import os

from pokyfriends.settings import BASE_DIR, ENVIRONMENT

# Pokyfriends
REMOTE_ADDR_HEADER = os.environ.get("POKY_REMOTE_ADDR_HEADER", "REMOTE_ADDR")
STATIC_ROOT = os.path.join(BASE_DIR, "website", "static")
SITE_URL = "https://pokyfriends.com" if ENVIRONMENT != "DEV" else "http://django.pi:8000"

# C Dos Blog
BLOG_ROOT = "blarg"

# C Dos Gallery
GAL_ROOT = "argle"

# C Dos Organize
ORG_DATA_PATH = os.path.join(STATIC_ROOT, "priv", "cdosorganize-data.json")

# C Dos Upload
UPL_ROOT = os.path.join(STATIC_ROOT, "cdosupload", "upload")
