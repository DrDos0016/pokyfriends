from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

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

class Post(models.Model):
    (PRIVACY_PUBLIC, PRIVACY_UNLISTED, PRIVACY_PASSWORD, PRIVACY_PRIVATE) = (1, 2, 3, 4)
    PRIVACY_CHOICES = (
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

    title           = models.CharField(max_length=100)
    author = "Dr. Dos"
    slug            = models.SlugField(max_length=100)
    icon = models.ForeignKey("Icon", null=True, blank=True, on_delete=models.SET_NULL)
    current_mood = models.CharField(max_length=100, blank=True)
    current_music = models.CharField(max_length=250, blank=True)
    summary         = models.CharField(max_length=250)
    css             = models.TextField(default="", blank=True)
    content         = models.TextField()
    source          = models.URLField(default="", blank=True)
    privacy         = models.IntegerField(choices=PRIVACY_CHOICES, default=PRIVACY_PUBLIC)
    schema          = models.IntegerField(choices=SCHEMA_CHOICES, default=SCHEMA_HTML)
    password = models.CharField(max_length=32, default="", blank=True)
    warnings = models.CharField(max_length=250, blank=True)
    date = models.DateTimeField()
    modification_date = models.DateTimeField(help_text="Date DB entry was last modified", auto_now=True)
    revision_date = models.DateTimeField(help_text="Date article content was last revised", default=None, null=True, blank=True)
    revision_details = models.TextField(help_text="Reference for revisions made to the article", default="", blank=True)
    likes = models.IntegerField(default=0)
    tags            = models.ManyToManyField("Tag")
    account         = models.CharField(max_length=32, default="dr-dos")
    preview_extension = models.CharField(max_length=5, default=".png")
    django_add_ons = models.CharField(choices=DJANGO_ADD_ON_CHOICES, null=True, max_length=32, help_text="Additional template tag/filter libraries to include")

    class Meta:
        app_label = "cdosblog"
        ordering = ("-date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/blog/post/{}/".format(self.slug)

    def get_static_path(self):
        return "cdosblog/{}/{}/{}/".format(self.account, self.date.year, self.slug)

    def get_preview_image_url(self):
        return "/static/{}preview{}".format(self.get_static_path(), self.preview_extension)
