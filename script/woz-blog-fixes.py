import json

import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokyfriends.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from django.template.defaultfilters import slugify  # noqa: E402

from cdosblog.models import *

def main():
    qs = Post.objects.filter(tags__name="Worlds of ZZT")

    for p in qs:
        p.content = p.content.replace("static 'blog/posts/{}/".format(p.pk), "static path|add:'")
        if p.css == "":
            p.css = "<style>.post-content img { max-width:100%; }</style>"
        p.save()
    return True


if __name__ == '__main__':
    main()
