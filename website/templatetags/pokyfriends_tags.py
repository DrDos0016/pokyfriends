from django import template

register = template.Library()

@register.inclusion_tag("website/subtemplate/meta.html", takes_context=True)
def meta_tags(context, title=None, description=None, image=None, url=None, author=None, kind=None):
    if context.get("project"):
        p = context["project"]
        (title, description, image) = (p.title, p.description, p.preview_image)

    image_path = image if image else "/static/og_image/pokyfriends.gif"
    if not image_path.startswith("http") and not image_path.startswith("/"):  # Translate plain filenames to standard directory
        image_path = "/static/og_image/{}".format(image)

    og_context = {}
    og_context["og_author"] = author if author else "Dr. Dos"
    og_context["og_description"] = description if description else "No description"
    og_context["og_type"] = kind if kind else "website"
    og_context["og_url"] = url if url else context["request"].build_absolute_uri()
    og_context["og_title"] = title if title else context.get("title", "Pokyfriends")
    og_context["og_image"] = "{}://{}{}".format(context["request"].scheme, context["request"].get_host(), image_path)
    return og_context


@register.inclusion_tag("website/subtemplate/retired-project.html")
def retired_project():
    return {}


@register.inclusion_tag("website/subtemplate/zeta-launcher.html")
def zeta_launcher(filename, save_db, launch_file="", engine="czoo439-dos.zip", zeta_version="1.0.7", commands=""):
    zeta_path = "/static/game/zzt/zeta-{}/".format(zeta_version)
    return {"filename": filename, "save_db": save_db, "launch_file": launch_file, "zeta_version": zeta_version, "engine": engine, "commands": commands}
