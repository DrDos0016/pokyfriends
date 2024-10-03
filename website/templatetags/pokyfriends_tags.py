from django import template

register = template.Library()

@register.inclusion_tag("website/subtemplate/meta.html", takes_context=True)
def meta_tags(context, author=None, description=None, kind=None, url=None, title=None, image=None):
    og_context = {}
    og_context["og_author"] = author if author else "Dr. Dos"
    og_context["og_description"] = description if description else "No description"
    og_context["og_type"] = kind if kind else "website"
    og_context["og_url"] = url if url else context["request"].build_absolute_uri()
    og_context["og_title"] = title if title else context.get("title", "Pokyfriends")
    og_context["og_image"] = image if image else "https://pokyfriends.com/static/global/pokyfriends-logo.png"
    return og_context


@register.inclusion_tag("website/subtemplate/retired-project.html")
def retired_project():
    return {}


@register.inclusion_tag("website/subtemplate/zeta-launcher.html")
def zeta_launcher(filename, save_db, launch_file="", engine="czoo439-dos.zip", zeta_version="1.0.7", commands=""):
    zeta_path = "/static/game/zzt/zeta-{}/".format(zeta_version)
    return {"filename": filename, "save_db": save_db, "launch_file": launch_file, "zeta_version": zeta_version, "engine": engine, "commands": commands}
