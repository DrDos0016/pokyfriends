from django import template
from django.template import Context, Template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def likes_widget(post):
    plural = "s" if post.likes != 1 else ""
    output = '<button class="likes-widget" data-slug="{{post.slug}}" title="Click to like this post"><img src="/static/global/favicon.png"> <div class="likes-count">{}</div> likes</button>'.format(post.likes, plural)
    return mark_safe(output)


@register.inclusion_tag("cdosblog/subtemplates/paginator_block.html", takes_context=True)
def paginator_block(context, page_obj):
    return {"page_obj": page_obj, "post": context.get("post")}


@register.inclusion_tag("cdosblog/subtemplates/render_post.html", takes_context=True)
def render_post(context, post, show_post=False):
    context["post"] = post
    context["show_post"] = show_post

    if show_post:
        if post.schema == post.SCHEMA_DJANGO:
            TEMPLATE_HEADER = "{% load static %}\n{% load blog_tags %}\n"
            add_ons = ""
            if post.django_add_ons:
                add_ons = "{{% load {} %}}\n".format(post.django_add_ons)  # Double braces are for python .format, not Django templating

            template = Template(TEMPLATE_HEADER + (add_ons) + post.content)
            sub_context = Context({"path": post.get_static_path()})
            context["parsed"] = template.render(sub_context)
        elif post.schema == post.SCHEMA_MARKDOWN:
            context["parsed"] = post.render_content()
        else:
            context["parsed"] = post.content
    return context


@register.inclusion_tag("cdosblog/subtemplates/img.html", takes_context=True)
def img(context, filename, title="", alt="", w="auto", h="auto", display="block", c=1):
    """ Click image for full size """
    static_path = context.get("path", "/") + filename
    if title and not alt:
        alt = title
    if alt and not title:
        title = alt

    return {"static_path": static_path, "w": w, "h": h, "title": title, "alt": alt, "display": display, "centered": c}
