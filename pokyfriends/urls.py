"""
URL configuration for pokyfriends project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import include, path

from website.views import *
from website.pokedex_ebooks_web_views import *
from website.tbr_views import *
from .settings import DEBUG
if DEBUG:
    from django.conf.urls.static import static

urlpatterns = [
    path("", Index_View.as_view(), name="index"),
    # Apps
    path('admin/', admin.site.urls),
    path('blog/', include("cdosblog.urls")),
    path('art/gallery/', include("cdosgallery.urls")),
    path('upload/', include("cdosupload.urls")),

    # Pages which require serverside processing
    path('doodle/pokedex-ebooks-web/', pokedex_ebooks_web_index, name="pokedex_ebooks_web_index"),
    path('doodle/pokedex-ebooks-web/comics/', pokedex_ebooks_web_comics, name="pokedex_ebooks_web_comics"),

    path('doodle/train-box-release/', train_box_release, name="train_box_release"),

    # Special Pages Unrelated to Pokyfriends
    #path('tf2-time/', tf2_time, name='tf2_time'),
    #path('openparty/', openparty, name="openparty"),

    # Standard Pages
    path("notepad/", notepad, name="notepad"),
    path("<slug:slug>/", Project_List_View.as_view(), name="project_list"),
    path("<slug:category_slug>/<slug:slug>/", Project_Detail_View.as_view(), name="project_details"),
]

if DEBUG:
    urlpatterns += static("/dos", document_root=os.path.join("/home/drdos/projects/pokyfriends/", "dos"))
