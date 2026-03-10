from django.urls import include, path

from .views import *

urlpatterns = [
    path("", Directory_Listing_View.as_view(), name="cdosupload"),
    path("edit", Edit_Text_View.as_view()),
]
