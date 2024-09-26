import glob  # Cohost
import os  # Cohost

from django.http import HttpResponse  # Cohost
from PIL import Image
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView

from website.models import Project

import time

# Create your views here.
class Index_View(TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Landing"
        context["TS"] = str(int(time.time()))
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
        context["title"] = self.object_list[0].get_category_display()
        return context

class Project_Detail_View(DetailView):
    context_object_name = "project"

    def get_template_names(self):
        return ["website/{}/{}.html".format(self.kwargs["category_slug"], self.kwargs["slug"])]

    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(slug=self.kwargs["slug"])


# TODO: This can be removed when Cohost is gone
def counter(request):
    SITE_ROOT = "/home/drdos/projects/pokyfriends/"
    VALID_KEYS = ["profile", "post"]
    counter_key = request.GET.get("key")

    if counter_key not in VALID_KEYS:
        return HttpResponse("Invalid key provided", status=404)

    match = glob.glob(os.path.join(SITE_ROOT, "website", "static", "cohost", "{}*".format(counter_key)))
    print("MATCH?", match)

    # Get the number
    if match:
        current = match[0]
        number = int(os.path.basename(current).split("-", maxsplit=1)[-1][:-4])
        number += 1
    else:
        number = 1

    # Generate the next image
    digits = str(number).zfill(5)
    im = Image.new("RGB", (len(digits)*32, 32))

    path = os.path.join(SITE_ROOT, "website", "static", "cohost")
    x = 0
    for d in digits:
        dim = Image.open(path + "/" + d + ".png")
        im.paste(dim, (x, 0))
        x += 32
    im.save(os.path.join(SITE_ROOT, "website", "static", "cohost", "{}-{}.png".format(counter_key, number)))

    # Serve the current image
    if not match:
        return HttpResponse("0")

    with open(current, "rb") as fh:
        raw = fh.read()

    os.remove(current)  # And remove the image
    return HttpResponse(raw, content_type="image/png")
