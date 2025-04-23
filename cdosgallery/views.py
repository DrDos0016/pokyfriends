from datetime import datetime
from django.core.exceptions import PermissionDenied

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .models import Artist, Character, Exhibit
from .forms import Gallery_Upload_Form

class Gallery_Browse_View(ListView):
    model = Exhibit
    paginate_by = 25

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.show_explicit = request.session.get("show_explicit_media", False)
        print("setup")

    def get_queryset(self):
        qs = Exhibit.objects.all()
        if not self.show_explicit:
            qs = qs.exclude(rating=Exhibit.EXPLICIT)
        qs = qs.order_by("-date", "-id")
        return qs

class Gallery_Browse_Artist_View(Gallery_Browse_View):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(artist__slug=self.kwargs["slug"]).order_by("-date", "-id")
        return qs


class Gallery_Browse_Character_View(Gallery_Browse_View):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(characters__slug=self.kwargs["slug"]).order_by("-date", "-id")
        return qs

class Gallery_Browse_Year_View(Gallery_Browse_View):
    def get_queryset(self):
        year = self.kwargs["year"] if self.kwargs["year"] != "unknown" else None
        qs = super().get_queryset()
        qs = qs.filter(date__year=year).order_by("-date", "-id")
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
        if not self.request.session.get("show_explicit_media", False):
            qs = qs.exclude(name__in=["Fate", "Fortune"])  # Sorry boys
        return qs


class Year_Browse_View(TemplateView):
    template_name = "cdosgallery/year_list.html"

    def get_context_data(self):
        context = super().get_context_data()
        reference_obj = Exhibit.objects.all().order_by("-date").first()
        if reference_obj:
            most_recent_year_of_art = reference_obj.date.year
        else:
            most_recent_year_of_art = datetime.now().year
        context["years"] = list(range(most_recent_year_of_art, 2005, -1))
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
        else:
            self.request.session.set_expiry(0)
            self.request.session["show_explicit_media"] = False
        return reverse("cdg_index")


class Upload_View(FormView):
    model = Exhibit
    form_class = Gallery_Upload_Form
    template_name = "cdosgallery/upload.html"

    def setup(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        super().setup(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def form_invalid(self, form):
        print("Bad form")
        return super().form_invalid(form)

    def form_valid(self, form):
        print("FORM VALID")
        post = form.save(commit=False)
        post.save()
        return redirect(post.get_absolute_url())
        #return super().form_valid(form)

    def get_success_url(self):
        return reverse("collection_manage_contents", kwargs={"slug": self.object.slug})
