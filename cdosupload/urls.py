from django.urls import include, path

from .views import *

urlpatterns = [
    path("", Directory_Listing_View.as_view()),
    path("edit", Edit_Text_View.as_view()),
]
