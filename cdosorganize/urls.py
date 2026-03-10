from django.urls import include, path

from .views import *

urlpatterns = [
    path("", CDosOrganize_View.as_view()),
]
