from datetime import datetime

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView
from django.views.generic import DetailView, ListView

from .models import Artist, Character, Exhibit

class Gallery_Browse_View(ListView):
    model = Exhibit
    paginate_by = 25

    def get_queryset(self):
        qs = Exhibit.objects.all().order_by("-date", "-id")
        return qs

class Gallery_Browse_Artist_View(Gallery_Browse_View):
    def get_queryset(self):
        qs = Exhibit.objects.filter(artist__slug=self.kwargs["slug"]).order_by("-date", "-id")
        return qs


class Gallery_Browse_Character_View(Gallery_Browse_View):
    def get_queryset(self):
        qs = Exhibit.objects.filter(characters__slug=self.kwargs["slug"]).order_by("-date", "-id")
        return qs

class Gallery_Browse_Year_View(Gallery_Browse_View):
    def get_queryset(self):
        year = self.kwargs["year"] if self.kwargs["year"] != "unknown" else None
        qs = Exhibit.objects.filter(date__year=year).order_by("-date", "-id")
        return qs


class Artist_Browse_View(ListView):
    model = Artist

    def get_queryset(self):
        qs = Artist.objects.all().order_by("name")
        return qs


class Character_Browse_View(ListView):
    model = Character

    def get_queryset(self):
        qs = Character.objects.all().order_by("order", "name")
        return qs


class Year_Browse_View(TemplateView):
    template_name = "cdosgallery/year_list.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["years"] = list(range(datetime.now().year, 2005, -1))
        context["years"].append("unknown")
        return context


class Exhibit_View(DetailView):
    model = Exhibit
    context_object_name = "exhibit"

    def get_queryset(self):
        qs = Exhibit.objects.filter(slug=self.kwargs["slug"])
        return qs

    def get_context_data(self, object):
        context = super().get_context_data()
        context["images"] = context["exhibit"].images.all().order_by("id")
        if self.kwargs.get("image"):
            context["main"] = context["exhibit"].images.all()[self.kwargs["image"] - 1]
        else:
            context["main"] = context["exhibit"].images.last()
        return context


class Explicit_Settings_View(TemplateView):
    template_name = "cdosgallery/explicit_settings.html"

    def get_context_data(self):
        context = super().get_context_data()
        return context


class Explicit_Settings_Submit_View(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.POST.get("explicit_confirmation") == "confirmed":
            self.request.session.set_expiry(0)
            self.request.session["show_explicit_media"] = True
            return self.request.POST.get("next", "/art/gallery/")
        return reverse("cdg_index")
