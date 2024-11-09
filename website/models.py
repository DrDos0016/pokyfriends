from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    CATEGORY_CHOICES = (
        ("game", "Game"),
        ("bot", "Bot"),
        ("website", "Website"),
        ("doodle", "Doodle"),
        ("tool", "Tool"),
        ("art", "Art"),
        ("blog", "Blog"),
        ("misc", "Misc."),
    )

    title = models.CharField(help_text="Project title", max_length=255)
    slug = models.CharField(help_text="Project slug", max_length=255, editable=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=32)
    external_url = models.URLField(max_length=255, blank=True, default="")
    date = models.DateField(blank=True, null=True, default=None)
    show_date = models.BooleanField(default=True)
    description = models.TextField(default="", blank=True)
    preview_image = models.CharField(max_length=255, blank=True, default="pokyfriends.gif")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        output = "Project [{}]: {}".format(self.id, self.title)
        return output

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.external_url:
            return self.external_url
        return reverse("project_details", kwargs={"category_slug": self.category, "slug": self.slug})
