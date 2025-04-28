import glob
import os
import time

from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import DetailView, ListView

from website.models import Project

from.forms import CDosUpload_Upload_Form

class Directory_Listing_View(FormView):
    template_name = "cdosupload/directory-listing.html"
    form_class = CDosUpload_Upload_Form

    AVAILABLE_DIRECTORIES = {
        "dos": {"root": "/home/drdos/projects/pokyfriends/dos", "root_url": "https://pokyfriends.com/dos/"},
        "images": {"root": "/home/drdos/projects/pokyfriends/i.pokyfriends", "root_url": "https://i.pokyfriends.com/"},
    }


    def setup(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        super().setup(request, *args, **kwargs)
        self.success_url = request.get_full_path()
        self.dir = request.GET.get("dir", "dos")
        directory_info = self.AVAILABLE_DIRECTORIES[self.dir]
        self.root = directory_info["root"]
        self.root_url = directory_info["root_url"]
        self.subdir = request.GET.get("subdir", "")
        self.path = os.path.join(self.root, self.subdir)
        self.parent = os.path.normpath(os.path.join(self.path, ".."))
        self.parent_dir = "/".join(self.subdir.split("/")[:-1])
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
            info = {"phys_path": file, "basename": basename, "url": self.root_url + self.subdir + "/" + basename,
                "stat": stat,
                "mtime": datetime.fromtimestamp(stat.st_mtime),
                "directory": os.path.isdir(file)
            }

            if self.request.user.is_staff and self.request.GET.get("op") == "del" and self.request.GET.get("filename") == info["basename"]:
                os.remove(info["phys_path"])
            else:
                files_with_data.append(info)

        sort = self.request.GET.get("sort", "name")
        sort_dir = "desc"if sort.startswith("-") else "asc"
        if sort == "date":
            self.files = sorted(files_with_data, key=lambda k: k["mtime"], reverse=(sort_dir == "desc"))
        elif sort == "size":
            self.files = sorted(files_with_data, key=lambda k: k["stat"].st_size, reverse=(sort_dir == "desc"))
        else:  # name
            self.files = sorted(files_with_data, key=lambda k: k["basename"].lower(), reverse=(sort_dir == "desc"))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Directory Listing"
        context["TS"] = str(int(time.time()))
        context["files"] = self.files
        context["parent"] = self.parent.replace(self.root, "")
        context["parent_dir"] = self.parent_dir
        context["subdir"] = self.subdir
        context["path"] = self.path
        context["root_url"] = self.root_url
        if self.subdir:
            context["root_url"] = context["root_url"] + self.subdir + "/"
        context["upload_errors"] = self.upload_errors
        context["available_directories"] = self.AVAILABLE_DIRECTORIES
        context["dir"] = self.dir

        return context

    def form_valid(self, form):
        self.get_file_directory()
        if form.process(self.root, self.subdir):
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        self.get_file_directory()
        return super().form_invalid(form)
