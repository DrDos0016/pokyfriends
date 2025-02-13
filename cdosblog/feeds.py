from datetime import datetime

from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.urls import reverse
from django.template.defaultfilters import slugify

from cdosblog.models import Post


class Base_Feed(Feed):
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return item.get_absolute_url()


class Blog_Feed(Base_Feed):
    title = "C:\Dos\Blog"
    link = "/blog/"
    description = "Dr. Dos's Blog"

    def items(self):
        return Post.objects.public().order_by("-date")[:25]

    def item_pubdate(self, item):
        return item.date

    def item_author_name(self, item):
        return item.author
