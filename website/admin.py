from django.contrib import admin

# Register your models here.
from website.models import *
from cdosblog.models import *
from cdosgallery.models import *

admin.site.register(Project)
admin.site.register(Exhibit)
admin.site.register(Artist)
admin.site.register(Character)
admin.site.register(Image)
admin.site.register(Source)
admin.site.register(Tag)
admin.site.register(Icon)
admin.site.register(Post)
admin.site.register(Comment)
