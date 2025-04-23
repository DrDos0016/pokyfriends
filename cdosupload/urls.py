from django.urls import include, path

from .views import *

urlpatterns = [
    path("", Directory_Listing_View.as_view())
]
