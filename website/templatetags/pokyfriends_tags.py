from django import template

register = template.Library()

@register.inclusion_tag("website/subtemplate/retired-project.html")
def retired_project():
    return {}


@register.inclusion_tag("website/subtemplate/zeta-launcher.html")
def zeta_launcher(filename, save_db, launch_file="", engine="czoo439-dos.zip", zeta_version="1.0.7", commands=""):
    zeta_path = "/static/game/zzt/zeta-{}/".format(zeta_version)
    return {"filename": filename, "save_db": save_db, "launch_file": launch_file, "zeta_version": zeta_version, "engine": engine, "commands": commands}
