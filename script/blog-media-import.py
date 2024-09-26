import json
import glob
import shutil

import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokyfriends.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from django.template.defaultfilters import slugify  # noqa: E402

from cdosblog.models import *

ROOT = "/home/drdos/garage/posts/"

def main():

    qs = Post.objects.all().order_by("id")

    for post in qs:
        import_media(post)
        print("Imported media for post:", post.pk, post.title)


def import_media(post):
    if not os.path.isdir(os.path.join(ROOT, str(post.pk))):
        return True

    # Make slug-based directory
    dest = "/home/drdos/projects/pokyfriends/cdosblog/static/cdosblog/dr-dos/{}/{}".format(post.date.year, post.slug)
    os.makedirs(dest, exist_ok=True)

    files = glob.glob(os.path.join(ROOT, str(post.pk), "*.*"))
    for f in files:
        final_path = os.path.join(dest, os.path.basename(f))
        print(f, "|||", final_path)
        shutil.copyfile(f, final_path)
    return True

if __name__ == '__main__':
    main()
