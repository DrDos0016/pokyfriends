import os

from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

import markdown

# Create your models here.
class Icon(models.Model):
    title = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return "/static/cdosblog/icons/{}".format(self.filename)


class Tag(models.Model):
    name            = models.CharField(max_length=100)
    slug            = models.SlugField(max_length=100, default="", blank=True)

    class Meta:
        app_label = "cdosblog"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/blog/tag/{}/".format(self.slug)

    @mark_safe
    def get_link(self):
        return '<a href="{}">{}</a>'.format(self.get_absolute_url(), self.name)


class Post_Queryset(models.QuerySet):
    def reach(self, *args, **kwargs):
        """ Return the requested object if it exists, returning None if it doesn't """
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

    def public(self):
        return self.filter(privacy=Post.PRIVACY_PUBLIC)


class Post(models.Model):
    objects = Post_Queryset.as_manager()

    (PRIVACY_DRAFT, PRIVACY_PUBLIC, PRIVACY_UNLISTED, PRIVACY_PASSWORD, PRIVACY_PRIVATE) = (0, 1, 2, 3, 4)
    PRIVACY_CHOICES = (
        (PRIVACY_DRAFT, "Draft"),
        (PRIVACY_PUBLIC, "Public"),
        (PRIVACY_UNLISTED, "Unlisted"),
        (PRIVACY_PASSWORD, "Password Protected"),
        (PRIVACY_PRIVATE, "Private")
    )

    (SCHEMA_HTML, SCHEMA_MARKDOWN, SCHEMA_DJANGO) = (1, 2, 3)
    SCHEMA_CHOICES = (
        (SCHEMA_DJANGO, "Django"),
        (SCHEMA_HTML, "HTML"),
        (SCHEMA_MARKDOWN, "Markdown"),
    )

    DJANGO_ADD_ON_CHOICES = (
        ("zzt_tags", "ZZT Tags (scroll, zzt_img)"),
    )

    title = models.CharField(max_length=100)
    author = "Dr. Dos"
    slug = models.SlugField(max_length=100, default="-")
    icon = models.ForeignKey("Icon", default=1, on_delete=models.SET_DEFAULT)
    current_mood = models.CharField(max_length=100, blank=True)
    current_music = models.CharField(max_length=250, blank=True)
    summary = models.CharField(max_length=250, blank=True, default="")
    css = models.TextField(default="", blank=True)
    content = models.TextField()
    source = models.URLField(default="", blank=True)
    privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=PRIVACY_PUBLIC)
    schema = models.IntegerField(choices=SCHEMA_CHOICES, default=SCHEMA_MARKDOWN)
    password = models.CharField(max_length=32, default="", blank=True)
    warnings = models.CharField(max_length=250, blank=True)
    date = models.DateTimeField()
    modification_date = models.DateTimeField(help_text="Date DB entry was last modified", auto_now=True)
    revision_date = models.DateTimeField(help_text="Date article content was last revised", default=None, null=True, blank=True)
    revision_details = models.TextField(help_text="Reference for revisions made to the article", default="", blank=True)
    likes = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tag")
    account = models.CharField(max_length=32, default="dr-dos")
    preview_extension = models.CharField(max_length=5, default=".png")
    django_add_ons = models.CharField(choices=DJANGO_ADD_ON_CHOICES, null=True, blank=True, max_length=32, help_text="Additional template tag/filter libraries to include")

    class Meta:
        app_label = "cdosblog"
        ordering = ("-date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.privacy != self.PRIVACY_PASSWORD:
            self.password = ""
        if self.css and not self.css.startswith("<style>"):
            self.css = "<style>\n" + self.css + "</style>\n"
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/blog/post/{}/".format(self.slug)

    def get_admin_url(self):
        return "/admin/cdosblog/post/{}/change/".format(self.pk)

    def get_edit_url(self):
        return reverse("cdb_form_edit", args=[self.pk])

    def get_static_path(self):
        return "cdosblog/{}/{}/{}/".format(self.account, self.date.year, self.slug)

    def get_preview_image_url(self):
        return "/static/{}preview{}".format(self.get_static_path(), self.preview_extension)

    def has_preview_image(self):
        file_path = "/home/drdos/projects/pokyfriends/cdosblog/static/" + self.get_static_path() + "preview" + self.preview_extension
        if os.path.isfile(file_path):
            return True
        return False

    def render_content(self):
        if self.schema == Post.SCHEMA_MARKDOWN:
            return markdown.markdown(self.content)
        else:
            return self.content

    def lock(self, full=False):
        """ Blanks out fields for password protected posts where no password has been entered yet """
        self.current_mood = "Blank."
        self.current_music = "4'33\""
        self.revision_date = None
        self.revision_details = ""
        self.content = ""
        # Additional content removal for private posts
        if full:
            self.title = "Untitled"
            self.author = "None"
            self.slug = "blank"
            self.warnings = ""
            self.date = datetime.utcnow()
            self.modification_date = None
            self.revision_date = None
            self.revision_details = ""
            # TODO: Tags still leak

    def get_schema_as_string(self):
        return "X"

    @cached_property
    def get_tags_string(self):
        output = ""
        for tag in self.tags.all().order_by("name"):
            output += "#" + tag.name + ", "
        return output



class Like(models.Model):
    ip = models.GenericIPAddressField()
    datetime = models.DateTimeField(auto_now=True)
    post = models.ForeignKey("Post", null=True, blank=True, on_delete=models.SET_NULL)
