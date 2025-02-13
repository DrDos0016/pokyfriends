from django.db import models
from django.utils.text import slugify

class Exhibit(models.Model):
    (CLEAN, EXPLICIT) = ("Clean", "Explicit")
    (VISIBLE, HIDDEN) = ("Visible", "Hidden")

    RATING_CHOICES = (
        (CLEAN, "Clean"),
        (EXPLICIT, "Explicit"),
    )

    VISIBILITY_CHOICES = (
        (VISIBLE, "Visible"),
        (HIDDEN, "Hidden"),
    )

    title = models.CharField(help_text="Exhibit Title", max_length=255)
    slug = models.CharField(help_text="Exhibit Slug", max_length=255, editable=False)
    description = models.TextField(help_text="Exhibit Description", default="", blank=True)
    rating = models.CharField(choices=RATING_CHOICES, max_length=10)
    visibility = models.CharField(choices=VISIBILITY_CHOICES, max_length=8)
    date = models.DateField(default=None, blank=True, null=True)

    # Related data
    sources = models.ManyToManyField("Source", default=None, blank=True)
    artist = models.ForeignKey("Artist", on_delete=models.SET_NULL, null=True)
    images = models.ManyToManyField("Image")
    characters = models.ManyToManyField("Character")

    def __str__(self):
        output = "Exhibit [{}]: {}".format(self.id, self.title)
        return output

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Exhibit, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/art/gallery/view/{}/".format(self.slug)

    def thumbnail(self):
        image = self.images.last()
        if image:
            return image.thumbnail()
        else:
            return "X"

    def get_citation(self):
        if self.date:
            year = self.date.year
        return f"{self.title} by {self.artist.name}{year}"

    def get_preview_image(self):
        if self.rating == "Explicit":
            return "/static/og_image/pokyfriends.gif"
        return "/static/" + self.thumbnail()


class Artist(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, blank=True)
    gallery = models.URLField(default="", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        output = self.name
        return output

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Artist, self).save(*args, **kwargs)


class Character(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    species = models.CharField(max_length=100)
    order = models.IntegerField(default=10)
    icon = models.CharField(max_length=100, default="", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        output = self.name
        return output

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Character, self).save(*args, **kwargs)

    def thumbnail(self):
        return "cdosgallery/art/th/" + self.icon


class Image(models.Model):
    filename = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        output = self.filename
        return output

    def thumbnail(self):
        return "cdosgallery/art/th/" + self.filename

    def static_image(self):
        return "cdosgallery/art/" + self.filename

class Source(models.Model):
    url = models.URLField(max_length=255)
    site = models.CharField(max_length=100, blank=True, default="")
