from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.
from .models import Post, Tag


class Post_List_View(ListView):
    model = Post
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.tag = self.kwargs.get("tag_slug")
        self.year = self.kwargs.get("year")
        self.title = "All Posts"
        self.tag_obj = None

    def get_queryset(self):
        qs = super().get_queryset()

        if self.tag:
            qs = qs.filter(tags__slug=self.tag)
            self.tag_obj = Tag.objects.filter(slug=self.tag).first()
        elif self.year:
            qs = qs.filter(date__year=self.year)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.title

        if self.tag_obj:
            context["title"] = "Posts tagged {}".format(self.tag_obj.name)
        if self.year:
            context["title"] = "Posts from {}".format(self.year)
        return context


class Post_Detail_View(DetailView):
    model = Post


def quick_and_dirty_tag_list(request):
    context = {"title": "All Tags"}
    context["tags"] = Tag.objects.all().order_by("name")
    return render(request, "cdosblog/quick-and-dirty-tag-list.html", context)


def quick_and_dirty_date_list(request):
    context = {"title": "All Dates"}
    current_year = datetime.now().year
    context["dates"] = []
    dates = Post.objects.all().only("date").order_by("-date")
    for d in dates:
        if (d.date.year not in context["dates"]):
            context["dates"].append(d.date.year)
    return render(request, "cdosblog/quick-and-dirty-date-list.html", context)


def quick_and_dirty_nav(request, slug, direction):
    start = Post.objects.filter(slug=slug).first()
    if start:
        dest = None
        if direction == "next":
            dest = Post.objects.filter(date__gt=start.date).order_by("date").first()
        else:
            dest = Post.objects.filter(date__lt=start.date).order_by("date").last()

        if dest:
            return redirect(dest.get_absolute_url())
    return redirect(start)


def quick_and_dirty_rss_landing(request):
    context = {"title": "RSS Feeds"}
    return render(request, "cdosblog/quick-and-dirty-rss-landing.html", context)
