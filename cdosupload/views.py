import glob
import os

from datetime import datetime

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView

from website.models import Project

import time

class Directory_Listing_View(TemplateView):
    template_name = "website/directory-listing.html"
    image_extensions = [".JPG", ".JPEG", ".GIF", ".PNG", ".WEBP", ".BMP"]

    def __init__(self):
        self.root = "/home/drdos/projects/pokyfriends/dos"
        self.root_url = "https://pokyfriends.com/dos/"
        self.subdir = ""

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.subdir = request.GET.get("subdir", "")
        self.path = os.path.join(self.root, self.subdir)
        self.parent = os.path.normpath(os.path.join(self.path, ".."))
        self.upload_errors = []
        if request.method != "POST":
            self.get_file_directory()

    def get_file_directory(self):
        files = glob.glob(os.path.join(self.path, "*"))
        files_with_data = []

        for file in files:
            basename = os.path.basename(file)
            m_time = ""
            stat = os.stat(file)
            info = {"phys_path": file, "basename": basename, "url": self.root_url + basename,
                "stat": stat,
                "mtime": datetime.fromtimestamp(stat.st_mtime),
                "directory": os.path.isdir(file)
            }

            if self.request.user.is_staff and self.request.GET.get("op") == "del" and self.request.GET.get("filename") == info["basename"]:
                os.remove(info["phys_path"])
            else:
                files_with_data.append(info)

        self.files = files_with_data

    def post(self, request, *args, **kwargs):
        if request.FILES.get("file"):
            uploaded_file = request.FILES.get("file")
            print(uploaded_file.name)

            destination_name = (request.POST.get("new_name") or uploaded_file.name)
            ext = destination_name.split(".")[-1].upper()
            print("EXT", ext)
            if ext in self.image_extensions:
                print("image upload!")
            destination_full_path = os.path.join(self.path, destination_name)

            if not self.request.POST.get("overwrite") and os.path.isfile(destination_full_path):
                self.upload_errors.append("{} already exists!".format(destination_full_path))
            else:
                with open(destination_full_path, 'wb+') as fh:
                    for chunk in uploaded_file.chunks():
                        fh.write(chunk)
                print("WROTE", destination_full_path)
        else:
            self.upload_errors.append("No file provided!")

        self.get_file_directory()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Directory Listing"
        context["TS"] = str(int(time.time()))
        context["files"] = self.files
        context["parent"] = self.parent.replace(self.root, "")
        context["subdir"] = self.subdir
        context["path"] = self.path
        context["upload_errors"] = self.upload_errors
        return context
