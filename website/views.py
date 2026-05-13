import glob
import os

from datetime import datetime

from django.http import HttpResponse  # Cohost
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView

from website.cdosorganize_views import *

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

@login_required
def notepad(request):
    context = {}
    NOTEBOOK_ROOT = "/home/drdos/projects/pokyfriends/dos/notebook/"
    notebooks = glob.glob(os.path.join(NOTEBOOK_ROOT, "*.txt"))
    default_notebook_path = os.path.join(NOTEBOOK_ROOT, "default.txt")
    requested_notebook_name = request.GET.get("notebook", "default.txt")
    filename = request.POST.get("filename")

    if default_notebook_path not in notebooks:
        with open(default_notebook_path, "w") as fh:
            print("WRITING", default_notebook_path)
            fh.write("This is the default notebook. It was automatically created.")

    # If making a new notebook, create it and switch to it
    if request.method == "POST" and request.POST.get("action") == "Create":
        if filename:
            with open(os.path.join(NOTEBOOK_ROOT, filename), "w") as fh:
                ts = str(datetime.now())[:19]
                raw = "[{}] Created notebook `{}`".format(ts, filename)
                fh.write(raw)
                return redirect("/notepad/?notebook=" + filename)

    notebook = requested_notebook_name
    active_notebook_path = os.path.join(NOTEBOOK_ROOT, notebook)

    with open(active_notebook_path) as fh:
        raw = fh.read()

    # Add a line
    if request.method == "POST" and request.POST.get("text"):
        text = request.POST.get("text")
        if request.POST.get("timestamp"):
            ts = str(datetime.now())[:19]
            raw = "[{}] {}\n\n{}".format(ts, text, raw)
        else:
            raw = "{}\n\n{}".format(text, raw)

        with open(active_notebook_path, "w") as fh:
            fh.write(raw)
    # Bulk write the entire file
    if request.method == "POST" and request.POST.get("bulk"):
        raw = request.POST.get("bulk")
        filename = request.POST.get("notebook")
        active_notebook_path = os.path.join(NOTEBOOK_ROOT, filename)

        with open(active_notebook_path, "w") as fh:
            fh.write(raw)
        return redirect("/notepad/?notebook=" + filename)
    elif "edit" in request.GET:  # Present entire file for bulk editing
        context["editing"] = True

    # Set up alternate notebooks
    context["alternate_notebooks"] = []
    for n in notebooks:
        alt = os.path.basename(n)
        context["alternate_notebooks"].append(alt)

    context["alternate_notebooks"] = sorted(context["alternate_notebooks"])

    context["notebook"] = notebook
    context["contents"] = raw
    context["size"] = len(raw)
    return render(request, "website/notepad.html", context)

@login_required
def dostop(request):
    context = {"title": "Dostop"}
    return render(request, "website/dostop.html", context)
