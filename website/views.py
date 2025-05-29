import glob
import os  # Cohost

from datetime import datetime

from django.http import HttpResponse  # Cohost
from PIL import Image
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView

from website.models import Project
from cdosblog.models import Post
from cdosgallery.models import Exhibit

import time

# Create your views here.
class Index_View(TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Landing"
        context["TS"] = str(int(time.time()))

        # Get latest things
        context["blog"] = Post.objects.filter(privacy=Post.PRIVACY_PUBLIC).order_by("-date").first()
        context["project"] = Project.objects.all().order_by("-date").first()
        context["exhibit"] = Exhibit.objects.filter(rating=Exhibit.CLEAN, visibility=Exhibit.VISIBLE).order_by("-date").first()
        return context


class Project_List_View(ListView):
    context_object_name = "projects"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if self.request.path.startswith("/art/") or self.request.path.startswith("/misc/"):
            self.sort_by_field = ["title"]
        else:
            self.sort_by_field = ["-date", "title"]

    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(category=self.kwargs["slug"]).order_by(*self.sort_by_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.object_list[0].get_category_display()
        if title in ["Art", "Misc."]:
            context["title"] = "Pokyfriends - " + title
        else:
            context["title"] = "Pokyfriends - " + title + "s"
        return context

class Project_Detail_View(DetailView):
    context_object_name = "project"

    def get_template_names(self):
        return ["website/{}/{}.html".format(self.kwargs["category_slug"], self.kwargs["slug"])]

    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(slug=self.kwargs["slug"])


def tf2_time(request):
    context = {}
    with open("/home/drdos/projects/pokyfriends/website/static/etc/tf2-playtime.log") as fh:
        lines = fh.readlines()
    context["line_count"] = 1
    lines = lines[:-14]
    return render(request, "museum_site/index.html", context)

def openparty(request):
    context = {}
    return render(request, "website/openparty.html", context)


