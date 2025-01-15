from datetime import datetime


from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

from website.settings import REMOTE_ADDR_HEADER

# Create your views here.
from .models import Like, Post, Tag, Icon
from .forms import Post_Form, Update_Post_Form


class Post_List_View(ListView):
    model = Post
    paginate_by = 10
    title = "All Posts"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.tag = self.kwargs.get("tag_slug")
        self.year = self.kwargs.get("year")
        self.tag_obj = None


    def get_queryset(self):
        qs = Post.objects.public()

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


@method_decorator(staff_member_required, name='dispatch')
class Master_Post_List_View(Post_List_View):
    paginate_by = 100
    template_name = "cdosblog/master_post_list.html"
    title = "Master Post List"

    def get_template_names(self):
        return self.template_name

    def get_queryset(self):
        qs = Post.objects.all()
        return qs


class Post_Detail_View(DetailView):
    model = Post

    def dispatch(self, request, *args, **kwargs):
        if request.method in ["POST", "GET"]:
            self.user_password = request.POST.get("user_password")
            return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if context["post"].privacy == Post.PRIVACY_PASSWORD:
            if self.user_password != context["post"].password:
                context["post"].lock()
                context["show_password_form"] = True
        if context["post"].privacy == Post.PRIVACY_PRIVATE:
            if not self.request.user.is_staff:
                context["post"].lock(full=True)
        return context


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


def post_like(request):
    """ Action performed when user clicks to like a blog post """
    pk = request.GET.get("pk", 0)
    post = Post.objects.filter(pk=pk).first()

    if not post:
        return JsonResponse({"success": 0})

    #print("IP HEADER", REMOTE_ADDR_HEADER)

    like, created = Like.objects.update_or_create(post_id=pk, ip=request.META.get(REMOTE_ADDR_HEADER))
    if created:
        post.likes += 1
        post.save()

    return JsonResponse({"success": 1, "total_likes": post.likes})



class Post_Create_View(CreateView):
    model = Post
    form_class = Post_Form

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["icons"] = Icon.objects.all()
        return context

    def form_invalid(self, form):
        print("Bad form")
        return super().form_invalid(form)

    def form_valid(self, form):
        print("FORM VALID")
        post = form.save(commit=False)
        post.date = datetime.utcnow()

        if post.css and not post.css.startswith("<style>"):
            post.css = "<style>\n{}</style>\n".format(post.css)

        post.save()
        return redirect(post.get_absolute_url())
        #return super().form_valid(form)

    def get_success_url(self):
        return reverse("collection_manage_contents", kwargs={"slug": self.object.slug})

class Post_Edit_View(UpdateView):
    model = Post
    form_class = Update_Post_Form
