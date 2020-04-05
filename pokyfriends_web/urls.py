from .views import *
import blackout.views
import bk_mario_maker.views
import chimp_or_chump.views
import clock.views
import gallery.views
import gen4_wifi.views
import maestro_tiles.views
import owo_whos_this.views
import pmdexplorers.views
import pokemon_type_chart_quiz.views
import pokepan_crystal.views
import stickers.views
import stitchr.views

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", generic, {"page":"index.html"}, name="generic"),
    path("info/<slug:slug>", generic, name="info"),
    path("contact", generic, {"page":"contact.html"}, name="contact"),
    path("support", generic, {"page":"support.html"}, name="support"),

    path("blackout", blackout.views.index, name="blackout"),
    path("blog/", include("blog.urls")),
    path("bkmario", bk_mario_maker.views.index, name="bk-mario-maker"),
    path("clock", clock.views.index, name="clock"),
    path("chimp-or-chump", chimp_or_chump.views.index, name="chimp-or-chump"),
    path("gallery/", include("gallery.urls")),
    path("maestro-tiles", maestro_tiles.views.index, name="maestro-tiles"),
    path("owo-whos-this", owo_whos_this.views.index, name="owo-whos-this"),
    path("pmdexplorers", pmdexplorers.views.index, name="pmd-explorers"),
    path("pokedex-ebooks/", include("pokedex_ebooks_web.urls"), name="pokedex-ebooks"),
    path("pokemon-size-quiz/", include("pokemon_size_quiz.urls"), name="pokemon-size-quiz"),
    path("pokemon-type-chart-quiz", pokemon_type_chart_quiz.views.index, name="pokemon-type-chart-quiz"),
    path("pokepan-crystal", pokepan_crystal.views.index, name="pokepan-crystal"),
    path("stickers", stickers.views.index, name="stickers"),
    path("stitchr", stitchr.views.index, name="stitchr"),
    path("train-box-release", include("train_box_release.urls")),
    path("wifi", gen4_wifi.views.index, name="gen4-wifi"),
    path("zzt/", include("zzt.urls")),
]
