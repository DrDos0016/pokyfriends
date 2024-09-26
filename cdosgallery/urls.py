from django.contrib import admin
from django.urls import include, path

from .views import *

urlpatterns = [
    path("", Gallery_Browse_View.as_view(), name="cdg_index"),
    path("artist/", Artist_Browse_View.as_view(), name="cdg_artist"),
    path("artist/<slug:slug>/", Gallery_Browse_Artist_View.as_view(), name="cdg_artist_browse"),
    path("character/", Character_Browse_View.as_view(), name="cdg_character"),
    path("character/<slug:slug>/", Gallery_Browse_Character_View.as_view(), name="cdg_character_browse"),
    path("explicit-settings/", Explicit_Settings_View.as_view(), name="cdg_explicit_settings"),
    path("explicit-settings/submit/", Explicit_Settings_Submit_View.as_view(), name="cdg_explicit_settings_submit"),
    path("year/", Year_Browse_View.as_view(), name="cdg_year"),
    path("view/<slug:slug>/", Exhibit_View.as_view(), name="cdg_exhibit_view"),
    path("view/<slug:slug>/<int:image>/", Exhibit_View.as_view(), name="cdg_exhibit_view_image"),
    path("year/<slug:year>/", Gallery_Browse_Year_View.as_view(), name="cdg_year_browse")
]
