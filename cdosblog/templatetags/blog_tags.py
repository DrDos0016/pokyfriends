from django import template
from django.template import Context, Template

register = template.Library()


@register.inclusion_tag("cdosblog/subtemplates/paginator_block.html", takes_context=True)
def paginator_block(context, page_obj):
    return {"page_obj": page_obj, "post": context.get("post")}

@register.inclusion_tag("cdosblog/subtemplates/render_post.html", takes_context=True)
def render_post(context, post, show_post=False):
    context["post"] = post
    context["show_post"] = show_post

    if show_post:
        if post.schema == post.SCHEMA_DJANGO:
            TEMPLATE_HEADER = "{% load static %}\n"
            add_ons = ""
            if post.django_add_ons:
                add_ons = "{{% load {} %}}\n".format(post.django_add_ons)  # Double braces are for python .format, not Django templating

            template = Template(TEMPLATE_HEADER + (add_ons) + post.content)
            sub_context = Context({"path": post.get_static_path()})
            context["parsed"] = template.render(sub_context)
        else:
            context["parsed"] = post.content
    return context
