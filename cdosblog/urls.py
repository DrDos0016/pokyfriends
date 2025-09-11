from django.contrib import admin
from django.urls import include, path

from .views import *
from .feeds import *

urlpatterns = [
    path("", Post_List_View.as_view(), name="cdb_index"),
    path("master-post-list/", Master_Post_List_View.as_view(), name="cdb_master_post_list"),
    path("tag/", quick_and_dirty_tag_list, name="cdb_tag"),
    path("tag/<slug:tag_slug>/", Post_List_View.as_view(), name="cdb_tag"),
    path("date/", quick_and_dirty_date_list, name="cdb_date"),
    path("date/<int:year>/", Post_List_View.as_view(), name="cdb_year"),
    path("post/form/create/", Post_Create_View.as_view(), name="cdb_form_create"),
    path("post/form/edit/<int:pk>/", Post_Edit_View.as_view(), name="cdb_form_edit"),
    path("post/<slug:slug>/", Post_Detail_View.as_view(), name="cdb_post"),
    path("post/<slug:slug>/previous/", quick_and_dirty_nav, {"direction": "previous"}, name="cdb_post_previous"),
    path("post/<slug:slug>/next/", quick_and_dirty_nav, {"direction": "next"}, name="cdb_post_next"),
    path("rss/", quick_and_dirty_rss_landing, name="cdb_rss"),
    path("rss/<slug:blog_name>/", Blog_Feed(), name="rss_blog"),
    path("process/comment/", process_comment, name="cdb_process_comment"),

    path("action/post-like/", post_like, name="post_like")
]
