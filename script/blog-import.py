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

def set_tags(d):
    if d.get("model") == "blog.tag":
        print(d)
        t = T(name=d["fields"]["name"])
        t.save()

def set_posts(d):
    if d.get("model") == "blog.post":
        print(d)
        """title           = models.CharField(max_length=100)
        author          = models.CharField(max_length=20, default="Dr. Dos", db_index=True)
        summary         = models.CharField(max_length=150, default="An exciting article you should read")
        content         = models.TextField()
        source          = models.URLField(default="", blank=True)
        timestamp       = models.DateTimeField()
        published       = models.BooleanField(default=True)
        spotlight       = models.BooleanField(default=True)
        tags            = models.ManyToManyField("Tag")"""

        p = Post()
        p.title = d["fields"]["title"]
        p.summary = d["fields"]["summary"]
        p.css = ""
        p.content = d["fields"]["content"]
        p.source = d["fields"]["source"]
        p.privacy = Post.PRIVACY_PUBLIC
        p.schema = Post.SCHEMA_HTML
        p.static_directory = slugify(p.title)
        p.date = d["fields"]["timestamp"]
        p.save()

        """
        summary         = models.CharField(max_length=250)
        css             = models.TextField(default="", blank=True)
        content         = models.TextField()
        source          = models.URLField(default="", blank=True)
        privacy         = models.IntegerField(choices=PRIVACY_CHOICES, default=PRIVACY_PUBLIC)
        schema          = models.IntegerField(choices=SCHEMA_CHOICES, default=SCHEMA_HTML)
        static_directory = models.CharField(max_length=120, default="", blank=True, help_text=("Name of directory where static files for this post are stored"))
        password = models.CharField(max_length=32, default="", blank=True)
        #content warnings?
        date = models.DateTimeField()
        modification_date = models.DateTimeField(help_text="Date DB entry was last modified", auto_now=True)
        revision_date = models.DateTimeField(help_text="Date article content was last revised", default=None, null=True, blank=True)
        revision_details = models.TextField(help_text="Reference for revisions made to the article", default="", blank=True)
        tags            = models.ManyToManyField("Tag")"""

def main():
    with open("blogs.json") as fh:
        raw = fh.read()
    data = json.loads(raw)

    for d in data:
        print(d.get("model"))
        #break
        #set_tags(d)
        set_posts(d)
        #set_tags()
        """
            # Add artist assoc
            if d["fields"]["artist"]:
                e.artist_id = (d["fields"]["artist"])
                e.save()

            # Add image assoc
            if d["fields"]["images"]:
                for foo in d["fields"]["images"]:

                e.images.add(foo)
        """
    return True


if __name__ == '__main__':
    main()
